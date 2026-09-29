# 5-Tier Verification Infrastructure Plan (`TEST_INFRA.md`)

- **Authored By**: `coba-03-opaque-e2e-test-architect` (Archetype 3 — Opaque-Box 5-Tier E2E Test Architect & BDD Synthesizer)
- **Cognitive Isolation Attestation**: Authored strictly from `ORIGINAL_REQUEST.md` and `PROJECT.md § Feature Inventory` with zero reads of `src/main/java/`.

## Verification Tiers

| Tier | Name | Scope & Assertions | Runner Command |
|---|---|---|---|
| **Tier 1** | **Static Contract & Anti-Pattern Scan** | Verifies `BigDecimal` + `RoundingMode.HALF_EVEN`, zero `double`/`float` types, zero `TODO`/`FIXME`/mock stubs. | `python3 verify_5_tiers.py` |
| **Tier 2** | **Functional Legacy Parity (`FI-01`..`FI-06`)** | Verifies all 6 business rules mined from `TRACE XSLT` and `SecOffice GuptaTD 4GL` (`ACCP`, `AB05`, `AM02`, `AM09`, `RC01`, `RR04`, `AC04`, `AM04`). | `python3 verify_5_tiers.py` |
| **Tier 3** | **Boundary & Precision Edge Cases** | Exact boundaries: `€100,000.00` vs `€100,000.01`; `10,000 ms` vs `10,001 ms`; `HALF_EVEN` ties (`0.005`, `0.015`, `0.025`, `0.035`). | `python3 verify_5_tiers.py` |
| **Tier 4** | **BDD Cucumber/Gherkin & ISO-20022 Suite** | Executes all 8 `Scenario Outline` rows in `src/test/resources/features/sepa_instant_cutoff.feature` authored for EuroBank's 1,500 Test Analysts. | `python3 verify_5_tiers.py` |
| **Tier 5** | **White-Box Concurrency, Lane 1 PII Hook & JVM** | Verifies `.agents/hooks/lane1_pii_iban_guard.py`, 100-thread concurrency determinism, and full `javac`/`java` JVM execution. | `python3 verify_5_tiers.py` |
