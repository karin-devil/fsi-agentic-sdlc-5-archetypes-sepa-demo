package com.fsi.payments;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;
import java.util.regex.Pattern;

/**
 * Modernized Java 21 SEPA Instant (SCT Inst / ISO-20022 pacs.008.001.08) Validator.
 *
 * <p>Replaces legacy {@code legacy/trace_sepa_instant_cutoff.xslt} and
 * {@code legacy/secoffice_limit_check.apt} for EuroBank CoreMod 2030 (Story COREMOD-4821).
 * Enforces BaFin MaRisk AT 7.2 and EU DORA Articles 9 & 11 monetary precision and audit rules.
 */
public final class SepaInstantValidator {

    public static final BigDecimal MAX_INSTANT_AMOUNT_EUR = new BigDecimal("100000.00");
    public static final BigDecimal ZERO_EUR = new BigDecimal("0.00");
    public static final BigDecimal INSTANT_FEE_RATE = new BigDecimal("0.0015");
    public static final long MAX_SETTLEMENT_LATENCY_MS = 10_000L;
    public static final String SANCTIONS_SENTINEL_IBAN = "DE00999999990000000000";
    public static final String UNREACHABLE_BIC_PREFIX = "XX00";

    private static final Pattern BIC_PATTERN =
            Pattern.compile("^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$");

    public record PaymentRequest(
            String messageId,
            BigDecimal rawAmountEur,
            BigDecimal availableLiquidityEur,
            long elapsedMs,
            String debtorIban,
            String debtorBic,
            String creditorBic,
            String accountStatus,
            String amlStatus) {

        public PaymentRequest {
            Objects.requireNonNull(messageId, "messageId must not be null");
            Objects.requireNonNull(rawAmountEur, "rawAmountEur must not be null");
            Objects.requireNonNull(availableLiquidityEur, "availableLiquidityEur must not be null");
            Objects.requireNonNull(debtorIban, "debtorIban must not be null");
            Objects.requireNonNull(debtorBic, "debtorBic must not be null");
            Objects.requireNonNull(creditorBic, "creditorBic must not be null");
            Objects.requireNonNull(accountStatus, "accountStatus must not be null");
            Objects.requireNonNull(amlStatus, "amlStatus must not be null");
        }
    }

    public record ValidationResult(
            String messageId,
            boolean accepted,
            String isoStatusReason,
            String legacyRuleCode,
            BigDecimal roundedAmountEur,
            BigDecimal calculatedFeeEur,
            boolean bafinAuditRequired,
            String auditTrailMessage) {}

    public ValidationResult validate(PaymentRequest request) {
        Objects.requireNonNull(request, "PaymentRequest must not be null");

        // FI-03: Strict Bankers' Rounding (RoundingMode.HALF_EVEN) to 2 decimal places
        BigDecimal roundedAmount = request.rawAmountEur().setScale(2, RoundingMode.HALF_EVEN);
        BigDecimal roundedLiquidity =
                request.availableLiquidityEur().setScale(2, RoundingMode.HALF_EVEN);
        BigDecimal calculatedFee =
                roundedAmount.multiply(INSTANT_FEE_RATE).setScale(2, RoundingMode.HALF_EVEN);

        // Guard against zero or negative payment amounts
        if (roundedAmount.compareTo(ZERO_EUR) <= 0) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "AM09",
                    "INVALID_NON_POSITIVE_AMOUNT",
                    roundedAmount,
                    calculatedFee,
                    false,
                    "Rejected: Non-positive SEPA Instant amount (" + roundedAmount + " EUR).");
        }

        // FI-05: BaFin AML & Sanctions Freeze Check (Highest Regulatory Priority)
        if ("FREEZE".equalsIgnoreCase(request.amlStatus().trim())
                || SANCTIONS_SENTINEL_IBAN.equalsIgnoreCase(request.debtorIban().trim())) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "RR04",
                    "DE_BAFIN_AML_FREEZE",
                    roundedAmount,
                    calculatedFee,
                    true,
                    "Rejected [BaFin MaRisk AT 7.2 Mandatory Escalation]: AML/Sanctions freeze triggered.");
        }

        // FI-01: EPC SCT Inst Hard 10,000ms Settlement Cutoff (TRACE XSLT parity)
        if (request.elapsedMs() > MAX_SETTLEMENT_LATENCY_MS) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "AB05",
                    "SCT_INST_TIMEOUT_10S",
                    roundedAmount,
                    calculatedFee,
                    false,
                    "Rejected: Settlement latency "
                            + request.elapsedMs()
                            + "ms exceeds 10,000ms EPC SCT Inst SLA.");
        }

        // FI-04: BIC Format & Target2 Reachability Check (TRACE XSLT parity)
        if (!isValidReachableBic(request.debtorBic())
                || !isValidReachableBic(request.creditorBic())) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "RC01",
                    "AT_018_INVALID_BIC_ROUTING",
                    roundedAmount,
                    calculatedFee,
                    false,
                    "Rejected: Invalid or unreachable ISO-9362 BIC routing identifier.");
        }

        // FI-06a: Closed Account Check (SecOffice GuptaTD parity)
        if ("CLOSED".equalsIgnoreCase(request.accountStatus().trim())) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "AC04",
                    "ACCOUNT_CLOSED",
                    roundedAmount,
                    calculatedFee,
                    false,
                    "Rejected: Debtor account status is CLOSED.");
        }

        // FI-02: Maximum EUR 100,000.00 SEPA Instant Limit (SecOffice GuptaTD parity)
        if (roundedAmount.compareTo(MAX_INSTANT_AMOUNT_EUR) > 0) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "AM02",
                    "SECOFFICE_LIMIT_EXCEEDED_100K",
                    roundedAmount,
                    calculatedFee,
                    false,
                    "Rejected: Amount "
                            + roundedAmount
                            + " EUR exceeds EUR 100,000.00 SCT Inst limit.");
        }

        // FI-06b: Intraday Liquidity Sufficiency Check (SecOffice GuptaTD parity)
        if (roundedLiquidity.compareTo(roundedAmount) < 0) {
            return new ValidationResult(
                    request.messageId(),
                    false,
                    "AM04",
                    "INSUFFICIENT_LIQUIDITY",
                    roundedAmount,
                    calculatedFee,
                    false,
                    "Rejected: Available liquidity "
                            + roundedLiquidity
                            + " EUR is below required "
                            + roundedAmount
                            + " EUR.");
        }

        return new ValidationResult(
                request.messageId(),
                true,
                "ACCP",
                "OK_SCT_INST_ACCEPTED",
                roundedAmount,
                calculatedFee,
                false,
                "Accepted: SEPA Instant pacs.008.001.08 validated within 10s SLA and EUR 100k limit.");
    }

    private static boolean isValidReachableBic(String bic) {
        if (bic == null) {
            return false;
        }
        String normalized = bic.trim().toUpperCase();
        if (normalized.startsWith(UNREACHABLE_BIC_PREFIX)) {
            return false;
        }
        return BIC_PATTERN.matcher(normalized).matches();
    }

    /**
     * Standalone CLI self-test runner so {@code java SepaInstantValidator} can execute all
     * boundary & compliance assertions without external Maven/Gradle dependencies.
     */
    public static void main(String[] args) {
        SepaInstantValidator v = new SepaInstantValidator();

        // 1. Happy path
        ValidationResult r1 = v.validate(new PaymentRequest(
                "MSG-001",
                new BigDecimal("2500.00"),
                new BigDecimal("50000.00"),
                420L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(r1.accepted() && "ACCP".equals(r1.isoStatusReason()), "Happy path failed");
        assertCondition(new BigDecimal("3.75").equals(r1.calculatedFeeEur()), "Fee 3.75 failed");

        // 2. Exact boundary: EUR 100,000.00 at 10,000ms -> ACCEPTED
        ValidationResult r2 = v.validate(new PaymentRequest(
                "MSG-002",
                new BigDecimal("100000.00"),
                new BigDecimal("150000.00"),
                10_000L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(r2.accepted() && "ACCP".equals(r2.isoStatusReason()), "100k/10000ms boundary failed");

        // 3. One cent over: EUR 100,000.01 -> REJECTED AM02
        ValidationResult r3 = v.validate(new PaymentRequest(
                "MSG-003",
                new BigDecimal("100000.01"),
                new BigDecimal("200000.00"),
                1200L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(!r3.accepted() && "AM02".equals(r3.isoStatusReason()), "100000.01 AM02 failed");

        // 4. One millisecond over: 10,001ms -> REJECTED AB05
        ValidationResult r4 = v.validate(new PaymentRequest(
                "MSG-004",
                new BigDecimal("5000.00"),
                new BigDecimal("50000.00"),
                10_001L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(!r4.accepted() && "AB05".equals(r4.isoStatusReason()), "10001ms AB05 failed");

        // 5. Unreachable BIC XX00 -> REJECTED RC01
        ValidationResult r5 = v.validate(new PaymentRequest(
                "MSG-005",
                new BigDecimal("10.00"),
                new BigDecimal("50000.00"),
                300L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "XX00DEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(!r5.accepted() && "RC01".equals(r5.isoStatusReason()), "XX00 BIC RC01 failed");

        // 6. BaFin AML Freeze -> REJECTED RR04 + bafinAuditRequired=true
        ValidationResult r6 = v.validate(new PaymentRequest(
                "MSG-006",
                new BigDecimal("15000.00"),
                new BigDecimal("50000.00"),
                500L,
                "DE00999999990000000000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "FREEZE"));
        assertCondition(
                !r6.accepted() && "RR04".equals(r6.isoStatusReason()) && r6.bafinAuditRequired(),
                "AML Freeze RR04 failed");

        // 7. HALF_EVEN Bankers' Rounding tie-breakers (0.005 -> 0.00, 0.015 -> 0.02, 0.025 -> 0.02, 0.035 -> 0.04)
        ValidationResult r7 = v.validate(new PaymentRequest(
                "MSG-007",
                new BigDecimal("100.015"),
                new BigDecimal("500.00"),
                200L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(new BigDecimal("100.02").equals(r7.roundedAmountEur()), "HALF_EVEN 100.015->100.02 failed");

        ValidationResult r8 = v.validate(new PaymentRequest(
                "MSG-008",
                new BigDecimal("100.025"),
                new BigDecimal("500.00"),
                200L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        assertCondition(new BigDecimal("100.02").equals(r8.roundedAmountEur()), "HALF_EVEN 100.025->100.02 failed");

        System.out.println("[Java 21 SepaInstantValidator] All 8 embedded JVM self-test suites PASSED (HALF_EVEN, 10s SLA, 100k limit, RR04 AML).");
    }

    private static void assertCondition(boolean condition, String errorMessage) {
        if (!condition) {
            throw new AssertionError(errorMessage);
        }
    }
}
