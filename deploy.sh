#!/usr/bin/env bash
# ==============================================================================
# One-Command Cloud Run Deployment Script for Regulated FSI 5-Archetype Demo
# Deploys the Interactive Workbench (workbench/) to Google Cloud Run
# ==============================================================================
set -euo pipefail

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}"
REGION="${GOOGLE_CLOUD_REGION:-europe-west3}"
SERVICE_NAME="${SERVICE_NAME:-fsi-agy-teamwork-demo}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "${STAGE_DIR}"' EXIT

cp "${SCRIPT_DIR}/workbench/app.py" "${STAGE_DIR}/app.py"
cp "${SCRIPT_DIR}/workbench/Dockerfile" "${STAGE_DIR}/Dockerfile"
mkdir -p "${STAGE_DIR}/demo_repo"
cp -r "${SCRIPT_DIR}/." "${STAGE_DIR}/demo_repo/"

echo "Deploying ${SERVICE_NAME} to project=${PROJECT_ID} region=${REGION}..."
gcloud run deploy "${SERVICE_NAME}" \
  --source="${STAGE_DIR}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
  --no-invoker-iam-check \
  --min-instances=1 \
  --max-instances=1 \
  --memory=1Gi \
  --cpu=1 \
  --timeout=300 \
  --quiet
