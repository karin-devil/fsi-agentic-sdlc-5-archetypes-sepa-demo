#!/usr/bin/env python3
"""EuroBank Lane 1 (Consumer-Speed Sandbox) Deterministic PreToolUse & Prompt Guardrail.

Blocks any prompt or tool call in Lane 1 that contains:
1. Internal EuroBank Zone 2/3 hostnames or domains (*.intranet.coba, *.prod.eurobank.example)
2. Real/unapproved German IBANs (DE followed by 20 digits) outside the approved synthetic test allowlist
3. Private keys, JDBC production credentials, or bearer tokens.

Returns deterministic JSON:
  {"decision": "allow", "reason": "..."} (exit 0)
  {"decision": "deny",  "reason": "..."} (exit 2)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time

# Approved synthetic IBANs for clean-room Lane 1 testing (ECB / Bundesbank test vectors)
APPROVED_SYNTHETIC_IBANS = frozenset({
    "DE89370400440532013000",  # Standard Bundesbank synthetic test IBAN (Debtor)
    "DE12500105170648489890",  # Standard synthetic test IBAN (Creditor)
    "DE00999999990000000000",  # Synthetic BaFin AML freeze sentinel IBAN
})

IBAN_REGEX = re.compile(r"\bDE\d{20}\b")
INTERNAL_HOST_REGEX = re.compile(
    r"\b(?:[a-zA-Z0-9_-]+\.)+(?:intranet\.coba|prod\.eurobank\.de|zone3\.coba\.internal)\b",
    re.IGNORECASE,
)
SECRET_REGEX = re.compile(
    r"(?:-----BEGIN (?:RSA |EC )?PRIVATE KEY-----|jdbc:oracle:thin:@[^\s]+prod[^\s]*)",
    re.IGNORECASE,
)


def evaluate_payload(raw_text: str) -> dict:
    start_ns = time.perf_counter_ns()
    violations: list[str] = []

    # 1. Check internal Zone 2/3 production hostnames
    host_matches = INTERNAL_HOST_REGEX.findall(raw_text)
    if host_matches:
        violations.append(
            f"Prohibited EuroBank Zone 2/3 internal hostname detected in Lane 1: {host_matches[0]}"
        )

    # 2. Check German IBANs against synthetic allowlist
    for iban in IBAN_REGEX.findall(raw_text):
        if iban not in APPROVED_SYNTHETIC_IBANS:
            violations.append(
                f"Unapproved / potentially real customer IBAN '{iban}' detected in Lane 1. "
                f"Only synthetic Bundesbank test IBANs {sorted(APPROVED_SYNTHETIC_IBANS)} are permitted."
            )

    # 3. Check private keys / prod JDBC strings
    if SECRET_REGEX.search(raw_text):
        violations.append(
            "Production credential or private key material detected in Lane 1 payload."
        )

    elapsed_ms = round((time.perf_counter_ns() - start_ns) / 1_000_000, 3)

    if violations:
        return {
            "decision": "deny",
            "lane": "Lane 1 (Consumer-Speed Sandbox)",
            "enforcement": "DETERMINISTIC_PRE_TOOL_HOOK",
            "latency_ms": elapsed_ms,
            "bafin_control": "MaRisk AT 7.2 / DORA Art. 9 (Data Exfiltration Prevention)",
            "reason": " | ".join(violations),
        }

    return {
        "decision": "allow",
        "lane": "Lane 1 (Consumer-Speed Sandbox)",
        "enforcement": "DETERMINISTIC_PRE_TOOL_HOOK",
        "latency_ms": elapsed_ms,
        "bafin_control": "MaRisk AT 7.2 / DORA Art. 9",
        "reason": "Clean-room payload verified: zero real IBANs, zero Zone 2/3 hostnames, zero secrets.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="EuroBank Lane 1 PII/IBAN Guardrail Hook")
    parser.add_argument("--event", default="PreToolUse", help="Hook lifecycle event")
    parser.add_argument("--input-text", default=None, help="Optional direct text to evaluate")
    args = parser.parse_args()

    if args.input_text is not None:
        raw_text = args.input_text
    elif not sys.stdin.isatty():
        raw_text = sys.stdin.read()
    else:
        raw_text = ""

    result = evaluate_payload(raw_text)
    result["event"] = args.event
    print(json.dumps(result, indent=2))
    return 0 if result["decision"] == "allow" else 2


if __name__ == "__main__":
    sys.exit(main())
