# Prompt 01: 5-Act `/teamwork-preview` SEPA Instant Brownfield Modernization

## Goal of Using This Prompt
Triggers the full 5-Archetype `/teamwork-preview` autonomous pipeline (Sentinel -> Explorer/Spanner Graph Spec Miner -> Dual-Track Armed CodMod Worker + Opaque-Box Test Architect -> 6-Eyes Reviewer, Challenger, Forensic Auditor & OSCAL Compliance Exporter).

## Copy-Paste Prompt
```text
/teamwork-preview Modernize the legacy SEPA Instant (SCT Inst) payment validation and routing logic from legacy/trace_sepa_instant_cutoff.xslt and legacy/secoffice_limit_check.apt into a clean Java 21 service (src/main/java/com/fsi/payments/SepaInstantValidator.java).

Requirements:
1. Preserve 100% of legacy business rules (10,000ms SCT Inst settlement cutoff -> AB05, EUR 100,000.00 limit -> AM02, non-positive guard -> AM09, ISO-9362 BIC routing & XX00 block -> RC01, BaFin AML/Sanctions freeze -> RR04 with mandatory audit flag, closed account -> AC04, and intraday liquidity check -> AM04).
2. Enforce Java 21 engineering rules (.agents/rules/fsi_java21_bafin_rules.md): strict BigDecimal with RoundingMode.HALF_EVEN (Bankers' Rounding) for all currency and 15 bps fee calculations — zero double/float types.
3. Build an opaque-box 5-Tier verification suite (Track 2) including Cucumber/Gherkin BDD scenarios for our 1,500 Test Analysts without reading the implementation code.
4. Execute the 6-Eyes Review, Empirical Challenger boundary checks, and Forensic Auditor hard binary veto, and export the signed NIST OSCAL 1.1.2 compliance dossier to build/dasy_compliance_dossier.json.
```
