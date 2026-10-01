# Empirical Challenger & Prevented Regressions Ledger (`DEAD_ENDS.md`)

- **Maintained By**: `fsi-05-forensic-auditor-dasy-gate` (Empirical Challenger Pillar)

## Prevented Regressions & Rejected Implementation Hypotheses

### Dead End #1: Using `RoundingMode.HALF_UP` Instead of `RoundingMode.HALF_EVEN`
- **Hypothesis Tested**: Standard commercial rounding (`HALF_UP`) on `€100.025`.
- **Why Rejected**: Legacy `SecOffice` Gupta Team Developer (`secoffice_limit_check.apt#L31`) uses `SalNumberRoundEven(nRawAmountEur, 2)` (Bankers' Rounding). Under `HALF_UP`, `100.025` rounds to `100.03`, creating a 1-cent reconciliation drift in `fsi-core-ledger` (`SPANNER: ledger_postings_v2`) on every even half-cent tie.
- **Resolution**: Enforced `RoundingMode.HALF_EVEN` in `SepaInstantValidator.java` and added explicit tie-breaker assertions (`100.015 -> 100.02` and `100.025 -> 100.02`) in Tier 3.

### Dead End #2: Evaluating 10-Second Timeout (`AB05`) Before BaFin AML Freeze (`RR04`)
- **Hypothesis Tested**: Evaluating `elapsedMs > 10_000L` as the first check (matching `trace_sepa_instant_cutoff.xslt` order) before `secoffice_limit_check.apt`.
- **Why Rejected**: When unifying `TRACE XSLT` and `SecOffice GuptaTD` into a single Java 21 microservice, evaluating timeout before AML freeze would allow a sanctioned/frozen IBAN (`DE00999999990000000000`) that arrived at `10,005 ms` to be rejected as a benign timeout (`AB05` with `bafinAuditRequired = false`) instead of triggering the mandatory BaFin MaRisk AT 7.2 compliance alert (`RR04` with `bafinAuditRequired = true`).
- **Resolution**: Placed `FI-05` (BaFin AML & Sanctions Freeze Check) immediately after the non-positive amount guard so `RR04` + `bafinAuditRequired = true` is guaranteed regardless of network latency.
