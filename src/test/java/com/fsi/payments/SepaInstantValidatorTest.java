package com.fsi.payments;

import java.math.BigDecimal;
import com.fsi.payments.SepaInstantValidator.PaymentRequest;
import com.fsi.payments.SepaInstantValidator.ValidationResult;

/**
 * Track 2 Opaque-Box 5-Tier E2E Verification Test Suite ({@code fsi-03-opaque-e2e-test-architect}).
 *
 * <p>Derived strictly from {@code .agents/teamwork/ORIGINAL_REQUEST.md} and
 * {@code .agents/teamwork/PROJECT.md § Feature Inventory} without reading implementation internals.
 */
public final class SepaInstantValidatorTest {

    public static void main(String[] args) {
        SepaInstantValidator validator = new SepaInstantValidator();
        int passed = 0;

        // Tier 2 & 3: Standard Acceptance
        ValidationResult ok = validator.validate(new PaymentRequest(
                "TX-101",
                new BigDecimal("2500.00"),
                new BigDecimal("50000.00"),
                420L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(ok.accepted() && "ACCP".equals(ok.isoStatusReason()) && "OK_SCT_INST_ACCEPTED".equals(ok.legacyRuleCode()), "TX-101 failed");
        passed++;

        // Tier 3: Exact Upper Boundary (EUR 100,000.00 & 10,000ms) -> ACCEPTED
        ValidationResult boundaryOk = validator.validate(new PaymentRequest(
                "TX-102",
                new BigDecimal("100000.00"),
                new BigDecimal("100000.00"),
                10_000L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(boundaryOk.accepted() && "ACCP".equals(boundaryOk.isoStatusReason()), "TX-102 exact boundary failed");
        passed++;

        // Tier 3: +0.01 EUR Over Limit (EUR 100,000.01) -> REJECTED AM02
        ValidationResult overLimit = validator.validate(new PaymentRequest(
                "TX-103",
                new BigDecimal("100000.01"),
                new BigDecimal("200000.00"),
                1200L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(!overLimit.accepted() && "AM02".equals(overLimit.isoStatusReason()) && "SECOFFICE_LIMIT_EXCEEDED_100K".equals(overLimit.legacyRuleCode()), "TX-103 AM02 failed");
        passed++;

        // Tier 3: +1ms Over Cutoff (10,001ms) -> REJECTED AB05
        ValidationResult overTime = validator.validate(new PaymentRequest(
                "TX-104",
                new BigDecimal("5000.00"),
                new BigDecimal("50000.00"),
                10_001L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(!overTime.accepted() && "AB05".equals(overTime.isoStatusReason()) && "SCT_INST_TIMEOUT_10S".equals(overTime.legacyRuleCode()), "TX-104 AB05 failed");
        passed++;

        // Tier 2: Unreachable BIC XX00 -> REJECTED RC01
        ValidationResult badBic = validator.validate(new PaymentRequest(
                "TX-105",
                new BigDecimal("10.00"),
                new BigDecimal("50000.00"),
                300L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "XX00DEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(!badBic.accepted() && "RC01".equals(badBic.isoStatusReason()) && "AT_018_INVALID_BIC_ROUTING".equals(badBic.legacyRuleCode()), "TX-105 RC01 failed");
        passed++;

        // Tier 4: BaFin AML Freeze -> REJECTED RR04 + bafinAuditRequired=true
        ValidationResult aml = validator.validate(new PaymentRequest(
                "TX-106",
                new BigDecimal("15000.00"),
                new BigDecimal("50000.00"),
                500L,
                "DE00999999990000000000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "FREEZE"));
        require(!aml.accepted() && "RR04".equals(aml.isoStatusReason()) && aml.bafinAuditRequired(), "TX-106 RR04 failed");
        passed++;

        // Tier 2: Closed Account -> REJECTED AC04
        ValidationResult closed = validator.validate(new PaymentRequest(
                "TX-107",
                new BigDecimal("8000.00"),
                new BigDecimal("50000.00"),
                450L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "CLOSED",
                "CLEAR"));
        require(!closed.accepted() && "AC04".equals(closed.isoStatusReason()) && "ACCOUNT_CLOSED".equals(closed.legacyRuleCode()), "TX-107 AC04 failed");
        passed++;

        // Tier 2: Insufficient Liquidity -> REJECTED AM04
        ValidationResult noLiq = validator.validate(new PaymentRequest(
                "TX-108",
                new BigDecimal("8000.00"),
                new BigDecimal("7999.99"),
                450L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(!noLiq.accepted() && "AM04".equals(noLiq.isoStatusReason()) && "INSUFFICIENT_LIQUIDITY".equals(noLiq.legacyRuleCode()), "TX-108 AM04 failed");
        passed++;

        // Tier 3: Zero/Negative Amount -> REJECTED AM09
        ValidationResult zeroAmt = validator.validate(new PaymentRequest(
                "TX-109",
                new BigDecimal("0.00"),
                new BigDecimal("50000.00"),
                100L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(!zeroAmt.accepted() && "AM09".equals(zeroAmt.isoStatusReason()), "TX-109 AM09 failed");
        passed++;

        // Tier 3: HALF_EVEN Bankers' Rounding tie cases
        ValidationResult roundDownEven = validator.validate(new PaymentRequest(
                "TX-110",
                new BigDecimal("50.025"),
                new BigDecimal("1000.00"),
                100L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(new BigDecimal("50.02").equals(roundDownEven.roundedAmountEur()), "TX-110 HALF_EVEN 50.025->50.02 failed");
        passed++;

        ValidationResult roundUpEven = validator.validate(new PaymentRequest(
                "TX-111",
                new BigDecimal("50.035"),
                new BigDecimal("1000.00"),
                100L,
                "DE89500105170532013000",
                "EUBKDEFFXXX",
                "DEUTDEFFXXX",
                "ACTIVE",
                "CLEAR"));
        require(new BigDecimal("50.04").equals(roundUpEven.roundedAmountEur()), "TX-111 HALF_EVEN 50.035->50.04 failed");
        passed++;

        System.out.println("[Opaque-Box E2E Test Suite] PASSED " + passed + "/11 test scenarios (0 failures).");
    }

    private static void require(boolean cond, String msg) {
        if (!cond) {
            throw new AssertionError(msg);
        }
    }
}
