# EuroBank AG (Tier-1 Regulated FSI) — Java 21 & BaFin MaRisk AT 7.2 / EU DORA Engineering Rules

> **Scope**: Mandatory repository-level engineering rules injected into all Antigravity (AGY) and Google ADK agent sessions across Lane 1 (Consumer-Speed Sandbox) and Lane 2 (Regulated Zone 2 Production).
> **Regulatory Baseline**: BaFin MaRisk AT 7.2 / BAIT, EU DORA (Regulation (EU) 2022/2554) Articles 9 & 11, and EPC SEPA Instant Credit Transfer (`SCT Inst` `pacs.008.001.08`).

---

## Rule 1: Strict Monetary Precision (`BigDecimal` + `HALF_EVEN`)
- **NEVER** use primitive or boxed floating-point types (`double`, `Double`, `float`, `Float`) for monetary amounts, exchange rates, liquidity balances, or fee calculations.
- **ALWAYS** use `java.math.BigDecimal` constructed from `String` literals and scaled explicitly to `2` decimal places using `java.math.RoundingMode.HALF_EVEN` (Bankers' Rounding) to maintain 100% parity with legacy `SecOffice` Gupta Team Developer `SalNumberRound(nVal, 2)` semantics.

## Rule 2: EPC SEPA Instant (`SCT Inst`) Cutoff & Limit Invariants
- **Maximum Settlement Latency (`FI-01`)**: `elapsedMs <= 10_000L` (10.000 seconds inclusive) is **ACCEPTED**. `elapsedMs > 10_000L` (e.g., `10_001L`) MUST be **REJECTED** with ISO-20022 reason code `AB05` (`TimeoutCreditorAgent`) and legacy rule code `SCT_INST_TIMEOUT_10S`.
- **Maximum Transaction Limit (`FI-02`)**: `amountEur <= 100000.00` (€100,000.00 inclusive) is **ACCEPTED**. `amountEur > 100000.00` (e.g., `€100,000.01`) MUST be **REJECTED** with ISO-20022 reason code `AM02` (`NotAllowedAmount`) and legacy rule code `SECOFFICE_LIMIT_EXCEEDED_100K`.
- **Non-Positive Amount Guard**: Any `amountEur <= 0.00` MUST be **REJECTED** with ISO-20022 reason code `AM09` (`WrongAmount`) and legacy rule code `INVALID_NON_POSITIVE_AMOUNT`.

## Rule 3: ISO-9362 BIC Routing & BaFin AML Sanctions Freeze
- **BIC Validation (`FI-04`)**: Both Debtor and Creditor BICs must match `^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$` and must not begin with unreachable routing prefix `XX00`. Invalid/unreachable BICs MUST be **REJECTED** with ISO-20022 reason code `RC01` (`BankIdentifierIncorrect`) and legacy code `AT_018_INVALID_BIC_ROUTING`.
- **BaFin AML / Sanctions Freeze (`FI-05`)**: If `amlStatus == "FREEZE"` or either IBAN matches the BaFin sanctions test sentinel (`DE00999999990000000000`), the transaction MUST be **REJECTED** immediately with ISO-20022 reason code `RR04` (`RegulatoryReason`), legacy code `DE_BAFIN_AML_FREEZE`, and `bafinAuditRequired = true`.
- **Account Status & Liquidity (`FI-06`)**: Closed accounts (`accountStatus == "CLOSED"`) reject with `AC04` (`ClosedAccountNumber` / `ACCOUNT_CLOSED`). Insufficient liquidity (`availableLiquidityEur < roundedAmountEur`) rejects with `AM04` (`InsufficientFunds` / `INSUFFICIENT_LIQUIDITY`).

## Rule 4: Zero Mock / Zero Stub Policy (Forensic Auditor Gate)
- Production code under `src/main/java/` must contain **zero** `TODO`, `FIXME`, `HACK`, or placeholder comments, and **zero** hardcoded mock responses.
- Every validation execution must return an immutable Java 21 `record` containing deterministic ISO-20022 and DASY/OSCAL audit metadata.
