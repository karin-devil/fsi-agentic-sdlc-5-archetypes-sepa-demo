# Prompt 03: Product Owner & Test Analyst BDD & Synthetic ISO-20022 Synthesizer

## Goal of Using This Prompt
Demonstrates **Persona 2 (1,500 Non-Coding Product Owners, Business Analysts & Test Analysts)** using `Archetype 3 (fsi-03-opaque-e2e-test-architect)` and the `fsi-bdd-synthesizer` skill inside the simplified `Antigravity-Business.code-profile` to generate Cucumber/Gherkin `.feature` suites and synthetic `pacs.008.001.08` test vectors.

## Copy-Paste Prompt
```text
Using fsi_03_opaque_e2e_test_architect and .agents/skills/fsi-bdd-synthesizer/SKILL.md:
Generate the Cucumber/Gherkin Scenario Outline suite (src/test/resources/features/sepa_instant_cutoff.feature) covering all 6 mined legacy business rules (FI-01 through FI-06) using only Bundesbank-approved synthetic test IBANs, and verify that all 8 BDD scenarios pass against SepaInstantValidator.
```
