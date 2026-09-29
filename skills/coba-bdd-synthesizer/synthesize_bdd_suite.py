#!/usr/bin/env python3
"""Persona 2 (1,500 POs & Test Analysts) — BDD & ISO-20022 Synthetic Payload Generator.

Generates:
1. `src/test/resources/features/sepa_instant_cutoff.feature`
2. `build/synthetic_pacs008_samples.json`
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

FEATURE_CONTENT = """# language: en
@AppRaMo2030 @APPRAMO-4821 @BaFin_MaRisk_AT_7_2 @DORA_Art_11
Feature: SEPA Instant (SCT Inst) Cutoff, EUR 100k Limit & BaFin AML Validation
  As a EuroBank Payment Operations & Test Analyst (CAPCom A-23)
  I want deterministic validation of ISO-20022 pacs.008.001.08 instant payments
  So that migrated Java 21 services preserve 100% parity with legacy TRACE XSLT and SecOffice GuptaTD 4GL.

  Background:
    Given the EuroBank Java 21 SepaInstantValidator is active with BigDecimal HALF_EVEN rounding
    And only Bundesbank-approved synthetic test IBANs are used in Lane 1

  @Boundary @FI-01 @FI-02 @FI-03 @FI-04 @FI-05 @FI-06
  Scenario Outline: Validate SEPA Instant pacs.008.001.08 settlement rules and boundaries
    When a SEPA Instant payment of "<amount_eur>" EUR is submitted with elapsed time <elapsed_ms> ms
    And debtor IBAN is "<debtor_iban>", debtor BIC is "<debtor_bic>", creditor BIC is "<creditor_bic>"
    And account status is "<account_status>", AML status is "<aml_status>", and liquidity is "<liquidity_eur>" EUR
    Then the validation decision MUST be "<accepted>"
    And the ISO-20022 status reason code MUST be "<iso_reason>"
    And the legacy rule code MUST be "<legacy_code>"
    And the HALF_EVEN rounded fee (15 bps) MUST be "<fee_eur>" EUR
    And the BaFin mandatory audit flag MUST be "<bafin_audit>"

    Examples:
      | amount_eur | elapsed_ms | debtor_iban            | debtor_bic  | creditor_bic | account_status | aml_status | liquidity_eur | accepted | iso_reason | legacy_code                   | fee_eur | bafin_audit |
      | 2500.00    | 420        | DE89370400440532013000 | COBADEFFXXX | DEUTDEFFXXX  | ACTIVE         | CLEAR      | 50000.00      | true     | ACCP       | OK_SCT_INST_ACCEPTED          | 3.75    | false       |
      | 100000.00  | 10000      | DE89370400440532013000 | COBADEFFXXX | DEUTDEFFXXX  | ACTIVE         | CLEAR      | 150000.00     | true     | ACCP       | OK_SCT_INST_ACCEPTED          | 150.00  | false       |
      | 100000.01  | 1200       | DE89370400440532013000 | COBADEFFXXX | DEUTDEFFXXX  | ACTIVE         | CLEAR      | 200000.00     | false    | AM02       | SECOFFICE_LIMIT_EXCEEDED_100K | 150.00  | false       |
      | 5000.00    | 10001      | DE89370400440532013000 | COBADEFFXXX | DEUTDEFFXXX  | ACTIVE         | CLEAR      | 50000.00      | false    | AB05       | SCT_INST_TIMEOUT_10S          | 7.50    | false       |
      | 10.00      | 300        | DE89370400440532013000 | COBADEFFXXX | XX00DEFFXXX  | ACTIVE         | CLEAR      | 50000.00      | false    | RC01       | AT_018_INVALID_BIC_ROUTING    | 0.02    | false       |
      | 15000.00   | 500        | DE00999999990000000000 | COBADEFFXXX | DEUTDEFFXXX  | ACTIVE         | FREEZE     | 50000.00      | false    | RR04       | DE_BAFIN_AML_FREEZE           | 22.50   | true        |
      | 8000.00    | 450        | DE89370400440532013000 | COBADEFFXXX | DEUTDEFFXXX  | CLOSED         | CLEAR      | 50000.00      | false    | AC04       | ACCOUNT_CLOSED                | 12.00   | false       |
      | 8000.00    | 450        | DE89370400440532013000 | COBADEFFXXX | DEUTDEFFXXX  | ACTIVE         | CLEAR      | 7999.99       | false    | AM04       | INSUFFICIENT_LIQUIDITY        | 12.00   | false       |
"""


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    feature_path = repo_root / "src" / "test" / "resources" / "features" / "sepa_instant_cutoff.feature"
    feature_path.parent.mkdir(parents=True, exist_ok=True)
    feature_path.write_text(FEATURE_CONTENT, encoding="utf-8")

    out_dir = repo_root / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    samples_path = out_dir / "synthetic_pacs008_samples.json"
    samples = {
        "schema": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08",
        "persona": "EuroBank CAPCom VDI (A-23) — 1,500 POs & Test Analysts",
        "synthetic_guardrail": "Verified by .agents/hooks/lane1_pii_iban_guard.py",
        "scenarios_generated": 8,
        "feature_file": str(feature_path.relative_to(repo_root)),
    }
    samples_path.write_text(json.dumps(samples, indent=2), encoding="utf-8")
    print(f"[BDD Synthesizer] Wrote Gherkin feature: {feature_path}")
    print(f"[BDD Synthesizer] Wrote ISO-20022 metadata: {samples_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
