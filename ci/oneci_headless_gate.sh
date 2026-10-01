#!/usr/bin/env bash
# ==============================================================================
# Persona 3 (OneCI DevOps Engineer A-17): Headless AGY CLI Quality Gate
# Enforces Lane 1 -> Lane 2 promotion rules before deploying to Regulated Zone 2
# ==============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

echo "================================================================================"
echo " [OneCI A-17 HEADLESS GATE] Lane 1 -> Lane 2 Promotion & DASY Verification"
echo "================================================================================"

echo "[Step 1/3] Executing 5-Tier Verification & Forensic Anti-Pattern Scan..."
python3 verify_5_tiers.py

echo ""
echo "[Step 2/3] Synthesizing & Verifying Persona 2 Cucumber/Gherkin BDD Suite..."
python3 .agents/skills/fsi-bdd-synthesizer/synthesize_bdd_suite.py

echo ""
echo "[Step 3/3] Exporting Signed DASY OSCAL 1.1.2 Compliance Dossier..."
python3 .agents/skills/dasy-oscal-exporter/export_dasy_oscal.py

echo "================================================================================"
echo " [OneCI A-17 GATE PASSED] Artifact promoted to Zone 2 Regulated Production!"
echo "================================================================================"
