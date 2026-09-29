# Complete Artifact Catalog — Descriptions, Strategic Goals & Verification Matrix

> **Purpose**: This catalog provides a structured breakdown of every artifact in this repository, explaining **what the artifact is**, **what strategic and technical goal it achieves**, **which SDLC persona uses it**, and **how to verify or execute it**.

---

## 1. The 5 Agent Archetypes (`agents/` & `.agents/agents/`)

### 1.1 `coba-01-sentinel-spec-refiner.md`
- **Path**: [`agents/coba-01-sentinel-spec-refiner.md`](agents/coba-01-sentinel-spec-refiner.md)
- **What It Is**: The entry-point agent archetype combining the `/teamwork-preview` **Sentinel** role with the **5-Stage Spec Pipeline** (`/ideate` → `/pm-grill-me` → `/write-prd` → `/red-team-prd` → `/decompose-epic`).
- **Strategic Goal of Using It**:
  1. **Stop "Garbage-In, Garbage-Out" Prompting**: Forces Socratic clarification (`/pm-grill-me`) on ambiguous banking requirements (rounding modes, boundary inclusivity, regulatory reason codes) *before* any code is written.
  2. **Create an Unalterable Audit Baseline**: Writes the verbatim request to `.agents/teamwork/ORIGINAL_REQUEST.md` so downstream coding agents cannot silently drop difficult requirements to make tests pass.
- **Target Persona**: Product Owners (POs), Business Analysts, and Lead Software Engineers.

### 1.2 `coba-02-explorer-doku-miner.md`
- **Path**: [`agents/coba-02-explorer-doku-miner.md`](agents/coba-02-explorer-doku-miner.md)
- **What It Is**: The **Legacy Spec Miner & Spanner Graph Doku Agent** archetype equipped with `mcp__spannercg`.
- **Strategic Goal of Using It**:
  1. **Solve the 10M+ LoC Context Window Bottleneck**: Instead of running slow, expensive `grep`/`glob` searches across massive monorepos (`>180,000` tokens), it queries **Cloud Spanner Graph (`EuroBankEnterpriseSDLCGraph`)** in `~182ms` (`1,420` tokens) to find exact cross-repo dependencies, Oracle/Spanner tables, and governing BaFin PDFs.
  2. **Automate Reverse-Engineering & Living Documentation**: Extracts hidden business logic from legacy `TRACE XSLT` and `SecOffice GuptaTD 4GL` files into `PROJECT.md § Feature Inventory` and keeps C4/Arc42 architecture diagrams (`docs/living_architecture_sepa.md`) continuously synchronized with code.
- **Target Persona**: Enterprise Architects, Brownfield Migration Engineers (`AppRaMo 2030`).

### 1.3 `coba-03-opaque-e2e-test-architect.md`
- **Path**: [`agents/coba-03-opaque-e2e-test-architect.md`](agents/coba-03-opaque-e2e-test-architect.md)
- **What It Is**: The **Track 2 Opaque-Box 5-Tier E2E Test Architect & BDD Synthesizer** archetype.
- **Strategic Goal of Using It**:
  1. **Eliminate Tautological AI Unit Tests**: When a single AI agent writes both production code and unit tests, it tests *what it wrote* rather than *what was specified*. By structurally forbidding `Archetype 3` from reading `src/main/java/`, Track 2 tests act as an independent, specification-driven oracle.
  2. **Empower 1,500+ Non-Coding Test Analysts**: Automatically translates mined requirements into human-readable **Cucumber/Gherkin `.feature` files** (`sepa_instant_cutoff.feature`) with synthetic ISO-20022 test tables.
- **Target Persona**: QA Engineers, Test Analysts (`CAPCom` VDI `A-23`), Product Owners.

### 1.4 `coba-04-armed-codmod-worker.md`
- **Path**: [`agents/coba-04-armed-codmod-worker.md`](agents/coba-04-armed-codmod-worker.md)
- **What It Is**: The **Track 1 Armed Modernization Worker (`CodMod` Java 21 Engineer)** archetype.
- **Strategic Goal of Using It**:
  1. **Enforce Single-Writer Principle**: In multi-agent workflows, allowing multiple agents to edit source code causes race conditions and regressions. Only `Archetype 4` holds write permissions on `src/main/java/`.
  2. **Guarantee Banking-Grade Java 21 Code**: Translates legacy XSLT and 4GL into immutable Java 21 records (`SepaInstantValidator.java`) strictly adhering to `.agents/rules/coba_java21_bafin_rules.md` (`BigDecimal` + `RoundingMode.HALF_EVEN`, zero `double`/`float`).
- **Target Persona**: Backend Java Engineers, Application Modernization Squads.

### 1.5 `coba-05-forensic-auditor-dasy-gate.md`
- **Path**: [`agents/coba-05-forensic-auditor-dasy-gate.md`](agents/coba-05-forensic-auditor-dasy-gate.md)
- **What It Is**: The **6-Eyes Reviewer, Empirical Challenger, Forensic Auditor & DASY OSCAL Gate** archetype.
- **Strategic Goal of Using It**:
  1. **Enforce a Non-Skippable Hard Binary Veto**: Audits the completed code and tests against `ORIGINAL_REQUEST.md` to guarantee zero silent scope reductions, zero `TODO`/`FIXME` stubs, zero mocked returns, and 100% boundary accuracy (`€100,000.00` vs `€100,000.01`, `10,000ms` vs `10,001ms`).
  2. **Automate Regulatory Release Sign-Off (`DASY`)**: Generates a SHA-256 signed **NIST OSCAL 1.1.2 compliance dossier** (`build/dasy_compliance_dossier.json`) mapped directly to **BaFin MaRisk AT 7.2** and **EU DORA Articles 9 & 11**.
- **Target Persona**: Risk & Compliance Officers (`DASY`), Security Architects, DevOps Release Engineers (`OneCI`).

---

## 2. Governance, Guardrails & Multi-Agent State Artifacts

| Artifact | Category | Goal of Using This Artifact |
|---|---|---|
| [`.agents/hooks.json`](.agents/hooks.json) & [`.agents/hooks/lane1_pii_iban_guard.py`](.agents/hooks/lane1_pii_iban_guard.py) | Deterministic Security Hook | **Prove Lane 1 Data Safety**: Demonstrates to CISO / Data Privacy teams that consumer-speed AI experimentation (Lane 1) is protected by a deterministic `<0.1ms` local hook that blocks real customer IBANs, `.intranet.coba` domains, and secrets (`exit code 2`) before any API call occurs. |
| [`.agents/rules/coba_java21_bafin_rules.md`](.agents/rules/coba_java21_bafin_rules.md) | Engineering Constitution | **Enforce Monetary & Regulatory Invariants**: Ensures every agent session automatically applies `BigDecimal` `RoundingMode.HALF_EVEN` and ISO-20022 reason codes without repetitive prompting. |
| [`.agents/teamwork/ORIGINAL_REQUEST.md`](.agents/teamwork/ORIGINAL_REQUEST.md) | State Machine | **Anchor Forensic Verification**: Preserves the exact initial prompt so the Forensic Auditor can detect any omitted requirement. |
| [`.agents/teamwork/PROJECT.md`](.agents/teamwork/PROJECT.md) | State Machine | **Trace Legacy-to-Modern Parity**: Documents the 6 mined rules (`FI-01`..`FI-06`) from legacy XSLT and GuptaTD 4GL with line-level traceability. |
| [`.agents/teamwork/TEST_INFRA.md`](.agents/teamwork/TEST_INFRA.md) | State Machine | **Define 5-Tier Verification Architecture**: Establishes the contract for Tiers 1–5 testing. |
| [`.agents/teamwork/GATE_STATUS.md`](.agents/teamwork/GATE_STATUS.md) | State Machine | **Record 6-Eyes Binary Verdict**: Captures the formal `PASS` / `VETO` checklist from Reviewer, Challenger, and Forensic Auditor. |
| [`.agents/teamwork/DEAD_ENDS.md`](.agents/teamwork/DEAD_ENDS.md) | State Machine | **Capture Prevented Regressions**: Documents why `HALF_UP` rounding and pre-AML timeout evaluation were rejected during adversarial testing. |
| [`.agents/teamwork/TEST_READY.md`](.agents/teamwork/TEST_READY.md) | State Machine | **Attest 100% Green Test Execution**: Records the empirical execution results across all 28 assertions, 11 JVM tests, and 8 BDD scenarios. |
| [`build/dasy_compliance_dossier.json`](build/dasy_compliance_dossier.json) | Regulatory Deliverable | **Automate BaFin & DORA Audits**: Provides a machine-verifiable OSCAL 1.1.2 JSON bundle with SHA-256 file hashes for automated release gating. |
