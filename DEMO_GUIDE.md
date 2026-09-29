# DEMO_GUIDE.md — 20-Minute 5-Act `/teamwork-preview` & 3-Persona Live Demo Runbook

> **Audience**: Head of SDLC, Lead AI Architect, CCoE Platform Lead, and Regulatory Assurance Lead.
> **Duration**: 20 Minutes (5 Acts × 4 Minutes).

---

## Act 1 (00:00–04:00): Sentinel Request Capture & Lane 1 PII/IBAN Guardrail Hook
- **Archetype Active**: [`agents/coba-01-sentinel-spec-refiner.md`](agents/coba-01-sentinel-spec-refiner.md)
- **What to Show**:
  1. Show [`.agents/teamwork/ORIGINAL_REQUEST.md`](.agents/teamwork/ORIGINAL_REQUEST.md) capturing the verbatim request before any code is written.
  2. Run the **Lane 1 PreToolUse PII/IBAN Guardrail Hook** ([`.agents/hooks/lane1_pii_iban_guard.py`](.agents/hooks/lane1_pii_iban_guard.py)) on an unapproved real IBAN + `.intranet.coba` hostname:
     ```bash
     python3 .agents/hooks/lane1_pii_iban_guard.py --event=PreToolUse \
       --input-text="Query oracle.intranet.coba for customer IBAN DE44500105175407324931"
     ```
  3. **Key Takeaway**: Deterministic local hook blocks sensitive data in `<0.1ms` with exit code `2` (`{"decision": "deny"}`) before a single token leaves the workstation.

## Act 2 (04:00–08:00): Spanner Graph Spec Mining & Living Documentation (`Doku Agent`)
- **Archetype Active**: [`agents/coba-02-explorer-doku-miner.md`](agents/coba-02-explorer-doku-miner.md)
- **What to Show**:
  1. Open [`legacy/trace_sepa_instant_cutoff.xslt`](legacy/trace_sepa_instant_cutoff.xslt) and [`legacy/secoffice_limit_check.apt`](legacy/secoffice_limit_check.apt).
  2. Show how `Archetype 2` queries [`data/spanner_graph/enterprise_sdlc_knowledge_graph.gql`](data/spanner_graph/enterprise_sdlc_knowledge_graph.gql) in `182ms` and extracts all 6 hidden business rules (`FI-01`..`FI-06`) into [`.agents/teamwork/PROJECT.md`](.agents/teamwork/PROJECT.md) and [`docs/living_architecture_sepa.md`](docs/living_architecture_sepa.md).

## Act 3 (08:00–13:00): Dual-Track Execution (Track 1 Java 21 Worker || Track 2 Opaque-Box Test Architect)
- **Archetypes Active**: [`agents/coba-04-armed-codmod-worker.md`](agents/coba-04-armed-codmod-worker.md) (Track 1) & [`agents/coba-03-opaque-e2e-test-architect.md`](agents/coba-03-opaque-e2e-test-architect.md) (Track 2)
- **What to Show**:
  1. Show [`src/main/java/com/coba/payments/SepaInstantValidator.java`](src/main/java/com/coba/payments/SepaInstantValidator.java) using immutable Java 21 `record` types and `BigDecimal` `RoundingMode.HALF_EVEN`.
  2. Show [`src/test/resources/features/sepa_instant_cutoff.feature`](src/test/resources/features/sepa_instant_cutoff.feature) generated for the **1,500 Product Owners & Test Analysts** (`profiles/Antigravity-Business.code-profile`).

## Act 4 (13:00–17:00): The 6-Eyes Gate — Reviewer, Empirical Challenger & Forensic Auditor Veto
- **Archetype Active**: [`agents/coba-05-forensic-auditor-dasy-gate.md`](agents/coba-05-forensic-auditor-dasy-gate.md)
- **What to Show**:
  1. Open [`.agents/teamwork/DEAD_ENDS.md`](.agents/teamwork/DEAD_ENDS.md) to show the two subtle banking bugs caught by the Empirical Challenger (`HALF_EVEN` vs `HALF_UP` ledger drift and `RR04` BaFin AML priority over `AB05` timeout).
  2. Open [`.agents/teamwork/GATE_STATUS.md`](.agents/teamwork/GATE_STATUS.md) showing the Forensic Auditor's 6-point binary `VERDICT: PASS`.

## Act 5 (17:00–20:00): 5-Tier Verification Execution & Signed NIST OSCAL 1.1.2 Compliance Dossier
- **What to Run**:
  ```bash
  bash run_all_coba_demos.sh
  ```
- **Key Takeaway**: All 5 Tiers (including real OpenJDK 21 JVM compilation & tests) pass 100%, emitting the SHA-256 signed [`build/dasy_compliance_dossier.json`](build/dasy_compliance_dossier.json) mapped to **BaFin MaRisk AT 7.2** and **EU DORA Articles 9 & 11**.
