---
name: dasy-oscal-exporter
description: "Compiles .agents/teamwork/ verification artifacts (ORIGINAL_REQUEST.md, PROJECT.md, GATE_STATUS.md, DEAD_ENDS.md, TEST_READY.md) into a cryptographically hashed OSCAL 1.1.2 JSON compliance dossier for EuroBank's DASY platform (BaFin MaRisk AT 7.2 & EU DORA Art. 9/11)."
---

# DASY OSCAL 1.1.2 Compliance Exporter Skill (`dasy-oscal-exporter`)

## Purpose
Automates regulatory evidence generation for **Enterprise DASY (Digital Assurance & Security) platform** at EuroBank. Instead of engineers manually filling out spreadsheets before a release, this skill reads the multi-agent `/teamwork-preview` state machine files and emits a machine-verifiable **NIST OSCAL 1.1.2 Assessment Results JSON dossier** (`build/dasy_compliance_dossier.json`).

## Usage
```bash
python3 .agents/skills/dasy-oscal-exporter/export_dasy_oscal.py
```

## Regulatory Controls Mapped
- **BaFin MaRisk AT 7.2 / BAIT**: Software change verification, 6-Eyes separation of duties, and deterministic monetary rounding (`BigDecimal` `HALF_EVEN`).
- **EU DORA Article 9 (Protection & Prevention)**: Lane 1 / Lane 2 data boundary enforcement and `PreToolUse` PII/IBAN guardrail verification.
- **EU DORA Article 11 (Detection & Forensic Auditability)**: Non-skippable Forensic Auditor binary gate (`GATE_STATUS.md`) and adversarial boundary testing (`TEST_READY.md`).
