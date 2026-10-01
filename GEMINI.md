# AGENTS.md — Agent Discovery & Execution Guide (`#spark-build`)

> **Repository Purpose**: Reference implementation of a **Regulated FSI 5-Archetype Agentic SDLC Factory** using **Antigravity (AGY)**, **Google ADK 2.0**, **Cloud Spanner Graph MCP**, and **NIST OSCAL 1.1.2** automated compliance for SEPA Instant (`SCT Inst` `pacs.008.001.08`) brownfield modernization (`XSLT` + `GuptaTD 4GL` → `Java 21`).
> **Spark Metadata**: `spark-build`, `spark-build-days`, `emea-asset`, `agentic-sdlc`, `antigravity`, `google-adk`, `fsi`, `banking`, `sepa-instant`, `bafin`, `dora`, `oscal`.

---

## 1. Quick Discovery Map for AI Agents

When an AI agent (Antigravity, Gemini CLI, Google ADK, Claude Code) inspects this repository, use the following canonical paths:

- **Agent Definitions (`/agents` & `/.agents/agents`)**:
  1. [`agents/fsi-01-sentinel-spec-refiner.md`](agents/fsi-01-sentinel-spec-refiner.md) — Captures `ORIGINAL_REQUEST.md` & runs 5-Stage Spec Pipeline (`/ideate` → `/pm-grill-me` → `/write-prd` → `/red-team-prd` → `/decompose-epic`).
  2. [`agents/fsi-02-explorer-doku-miner.md`](agents/fsi-02-explorer-doku-miner.md) — Queries Spanner Graph (`data/spanner_graph/enterprise_sdlc_knowledge_graph.gql`) & mines legacy `legacy/trace_sepa_instant_cutoff.xslt` and `legacy/secoffice_limit_check.apt` into `.agents/teamwork/PROJECT.md`.
  3. [`agents/fsi-03-opaque-e2e-test-architect.md`](agents/fsi-03-opaque-e2e-test-architect.md) — Track 2 Opaque-Box Test Architect (writes `SepaInstantValidatorTest.java` & `sepa_instant_cutoff.feature` without reading `src/main/java/`).
  4. [`agents/fsi-04-armed-codmod-worker.md`](agents/fsi-04-armed-codmod-worker.md) — Track 1 Exclusive Code Write-Owner (implements `src/main/java/com/fsi/payments/SepaInstantValidator.java`).
  5. [`agents/fsi-05-forensic-auditor-dasy-gate.md`](agents/fsi-05-forensic-auditor-dasy-gate.md) — 6-Eyes Reviewer, Empirical Challenger, Forensic Auditor (`GATE_STATUS.md`, `DEAD_ENDS.md`, `TEST_READY.md`) & OSCAL 1.1.2 Exporter (`build/dasy_compliance_dossier.json`).
- **Skills (`/skills` & `/.agents/skills`)**:
  - [`skills/pm-grill-me/SKILL.md`](skills/pm-grill-me/SKILL.md)
  - [`skills/sepa-modernization/SKILL.md`](skills/sepa-modernization/SKILL.md)
  - [`skills/fsi-bdd-synthesizer/SKILL.md`](skills/fsi-bdd-synthesizer/SKILL.md) (`python3 .agents/skills/fsi-bdd-synthesizer/synthesize_bdd_suite.py`)
  - [`skills/dasy-oscal-exporter/SKILL.md`](skills/dasy-oscal-exporter/SKILL.md) (`python3 .agents/skills/dasy-oscal-exporter/export_dasy_oscal.py`)
- **Prompts (`/prompts`)**:
  - [`prompts/01_teamwork_preview_sepa_modernization.md`](prompts/01_teamwork_preview_sepa_modernization.md)
  - [`prompts/02_engineer_5_stage_spec_pipeline.md`](prompts/02_engineer_5_stage_spec_pipeline.md)
  - [`prompts/03_business_analyst_bdd_synthesizer.md`](prompts/03_business_analyst_bdd_synthesizer.md)
  - [`prompts/04_ci_headless_forensic_audit_gate.md`](prompts/04_ci_headless_forensic_audit_gate.md)
- **Datasets & Legacy Inputs (`/data` & `/legacy`)**:
  - [`data/legacy/trace_sepa_instant_cutoff.xslt`](data/legacy/trace_sepa_instant_cutoff.xslt)
  - [`data/legacy/secoffice_limit_check.apt`](data/legacy/secoffice_limit_check.apt)
  - [`data/spanner_graph/enterprise_sdlc_knowledge_graph.gql`](data/spanner_graph/enterprise_sdlc_knowledge_graph.gql)
- **Machine-Readable Catalog**: [`agent-catalog.json`](agent-catalog.json) and [`llms.txt`](llms.txt)

---

## 2. Mandatory Verification Commands for Agents

Before concluding any task in this repository, always run:
```bash
bash run_all_fsi_demos.sh
```
or run the 5-Tier verification suite directly:
```bash
python3 verify_5_tiers.py
```
