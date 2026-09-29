# Immutable Sentinel Request Log (`ORIGINAL_REQUEST.md`)

- **Captured By**: `coba-01-sentinel-spec-refiner` (Archetype 1 — Sentinel & 5-Stage Spec Refiner)
- **Timestamp (UTC)**: `2026-09-29T19:45:00Z`
- **Target Initiative**: `EuroBank AppRaMo 2030 — Legacy Brownfield Modernization (Jira: APPRAMO-4821)`
- **Regulatory Scope**: `BaFin MaRisk AT 7.2 / BAIT`, `EU DORA (Reg. 2022/2554) Art. 9 & 11`, `EPC SEPA Instant (pacs.008.001.08)`

## Verbatim User Prompt
```text
/teamwork-preview Modernize the legacy SEPA Instant (SCT Inst) payment validation and routing logic from legacy/trace_sepa_instant_cutoff.xslt (TRACE XML gateway) and legacy/secoffice_limit_check.apt (SecOffice Gupta Team Developer 4GL) into a clean Java 21 service (src/main/java/com/coba/payments/SepaInstantValidator.java).

Requirements:
1. Preserve 100% of legacy business rules (10,000ms SCT Inst settlement cutoff -> AB05, EUR 100,000.00 limit -> AM02, non-positive guard -> AM09, ISO-9362 BIC routing & XX00 block -> RC01, BaFin AML/Sanctions freeze -> RR04 with mandatory audit flag, closed account -> AC04, and intraday liquidity check -> AM04).
2. Enforce EuroBank Java 21 engineering rules (.agents/rules/coba_java21_bafin_rules.md): strict BigDecimal with RoundingMode.HALF_EVEN (Bankers' Rounding) for all currency and 15 bps fee calculations — zero double/float types.
3. Build an opaque-box 5-Tier verification suite (Track 2) including Cucumber/Gherkin BDD scenarios for our 1,500 Test Analysts without reading the implementation code.
4. Execute the 6-Eyes Review, Empirical Challenger boundary checks, and Forensic Auditor hard binary veto, and export the signed DASY OSCAL 1.1.2 compliance dossier to build/dasy_compliance_dossier.json.
```
