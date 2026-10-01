# Multi-Agent Project Plan & Legacy Feature Inventory (`PROJECT.md`)

- **Authored By**: `fsi-02-explorer-doku-miner` (Archetype 2 — Explorer, Spec Miner & Spanner Graph Doku Agent)
- **Spanner Graph Query**: `EuroBankEnterpriseSDLCGraph` (`COREMOD-4821` — 4 hops traversed in `182ms`, `1,420` tokens vs. `>180,000` raw grep tokens)

---

## § 1. Feature Inventory (Mined from `TRACE XSLT` & `SecOffice GuptaTD 4GL`)

| Feature ID | Legacy Source File & Line | Mined Business Rule | ISO-20022 Code | Legacy Rule Code | Target Java 21 Contract |
|---|---|---|---|---|---|
| **FI-01** | `legacy/trace_sepa_instant_cutoff.xslt#L24-L29` | Reject if `elapsedMs > 10000` (10.000s EPC SCT Inst SLA cutoff; `10000` is ACCEPTED) | `AB05` | `SCT_INST_TIMEOUT_10S` | `elapsedMs > 10_000L` |
| **FI-02** | `legacy/secoffice_limit_check.apt#L35-L39`, `#L53-L57` | Reject if `roundedAmountEur <= 0.00` (`AM09`) or `roundedAmountEur > 100000.00` (`AM02`; `100000.00` is ACCEPTED) | `AM09` / `AM02` | `INVALID_NON_POSITIVE_AMOUNT` / `SECOFFICE_LIMIT_EXCEEDED_100K` | `BigDecimal("100000.00")` comparison |
| **FI-03** | `legacy/secoffice_limit_check.apt#L31-L32` | Bankers' Rounding (`SalNumberRoundEven(..., 2)`) on amount, liquidity, and `0.0015` (15 bps) fee | N/A | N/A | `BigDecimal.setScale(2, RoundingMode.HALF_EVEN)` |
| **FI-04** | `legacy/trace_sepa_instant_cutoff.xslt#L32-L36` | Debtor & Creditor BIC must match ISO-9362 (8 or 11 chars) and not start with `XX00` | `RC01` | `AT_018_INVALID_BIC_ROUTING` | `BIC_PATTERN` + `!startsWith("XX00")` |
| **FI-05** | `legacy/secoffice_limit_check.apt#L41-L46` | Highest priority regulatory check: if `amlStatus == "FREEZE"` or IBAN is `DE00999999990000000000`, reject and set `bafinAuditRequired = true` | `RR04` | `DE_BAFIN_AML_FREEZE` | `bafinAuditRequired = true` |
| **FI-06** | `legacy/secoffice_limit_check.apt#L48-L63` | Reject if `accountStatus == "CLOSED"` (`AC04`) or `availableLiquidityEur < roundedAmountEur` (`AM04`) | `AC04` / `AM04` | `ACCOUNT_CLOSED` / `INSUFFICIENT_LIQUIDITY` | `ValidationResult` record |

---

## § 2. Dual-Track Execution Topology

1. **Track 1 — Armed Implementation (`fsi-04-armed-codmod-worker`)**:
   - Exclusive write owner of `src/main/java/com/fsi/payments/SepaInstantValidator.java`.
2. **Track 2 — Opaque-Box Verification (`fsi-03-opaque-e2e-test-architect`)**:
   - Exclusive write owner of `src/test/java/com/fsi/payments/SepaInstantValidatorTest.java` and `src/test/resources/features/sepa_instant_cutoff.feature`.
   - Cognitively isolated from Track 1 implementation code.
3. **6-Eyes Gate & DASY Exporter (`fsi-05-forensic-auditor-dasy-gate`)**:
   - Executes Reviewer + Challenger + Forensic Auditor binary veto and generates `build/dasy_compliance_dossier.json`.
