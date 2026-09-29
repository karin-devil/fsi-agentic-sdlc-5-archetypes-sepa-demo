---
name: coba-bdd-synthesizer
description: "Persona 2 Skill (1,500 POs & Test Analysts on CAPCom VDI A-23): Synthesizes Cucumber/Gherkin .feature specifications and synthetic ISO-20022 pacs.008.001.08 XML test payloads directly from PRD / Feature Inventory."
---

# EuroBank BDD & Synthetic ISO-20022 Test Synthesizer (`coba-bdd-synthesizer`)

## Target Persona
Designed for EuroBank's **1,500 Product Owners (POs), Business Analysts, and Test Analysts** operating in the simplified `Antigravity-Business.code-profile` on Windows VDI (`CAPCom` `A-23`).

## Usage
```bash
python3 .agents/skills/coba-bdd-synthesizer/synthesize_bdd_suite.py
```

## Outputs
1. `src/test/resources/features/sepa_instant_cutoff.feature` — Complete Cucumber/Gherkin `Scenario Outline` covering all 6 legacy business rules and boundary cases.
2. `build/synthetic_pacs008_samples.json` — Synthetic ISO-20022 `pacs.008.001.08` test vectors using only Bundesbank-approved synthetic IBANs (`DE89370400440532013000`).
