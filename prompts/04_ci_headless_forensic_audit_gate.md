# Prompt 04: DevOps Headless CI/CD Gate & NIST OSCAL 1.1.2 Compliance Dossier Exporter

## Goal of Using This Prompt
Demonstrates **Persona 3 (DevOps / CI Engineer & Compliance Officer)** running `Archetype 5 (fsi-05-forensic-auditor-dasy-gate)` in headless CI/CD (`ci/oneci_headless_gate.sh`) to enforce the 6-Eyes Forensic Auditor veto and generate the SHA-256 signed NIST OSCAL 1.1.2 compliance dossier (`build/dasy_compliance_dossier.json`).

## Copy-Paste Prompt
```text
Execute the headless CI/CD promotion gate (bash ci/oneci_headless_gate.sh):
1. Run all 5 Verification Tiers (verify_5_tiers.py), including the OpenJDK 21 JVM test suites and Lane 1 PreToolUse PII/IBAN Guardrail hook verification.
2. Verify that .agents/teamwork/GATE_STATUS.md records VERDICT: PASS with zero TODOs, zero mocks, and zero floating-point types.
3. Export the signed NIST OSCAL 1.1.2 compliance dossier (build/dasy_compliance_dossier.json) and display its SHA-256 attestation signature.
```
