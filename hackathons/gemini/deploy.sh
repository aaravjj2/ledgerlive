#!/usr/bin/env bash
# ── LedgerLive — Google Cloud Run Deployment ──────────────────────
# Deploys the FastAPI backend to Cloud Run with Gemini Live API integration.
#
# Prerequisites:
#   1. gcloud CLI authenticated: gcloud auth login
#   2. Secrets created in Secret Manager:
#      - GEMINI_API_KEY
#      - SECRET_KEY
#   3. APIs enabled: Cloud Run, Cloud Build, Artifact Registry, Secret Manager
#
# Usage:
#   ./hackathons/gemini/deploy.sh
#   REGION=europe-west1 ./hackathons/gemini/deploy.sh

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-ledgerlive-gemini}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="ledgerlive-api"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "=== LedgerLive Cloud Run Deployment ==="
echo "  Project:  ${PROJECT_ID}"
echo "  Region:   ${REGION}"
echo "  Service:  ${SERVICE_NAME}"
echo ""

# ── Step 1: Enable required APIs ──────────────────────────────────
echo "[1/5] Enabling required Google Cloud APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  --project="${PROJECT_ID}" \
  --quiet

# ── Step 2: Verify secrets exist ──────────────────────────────────
echo "[2/5] Verifying secrets in Secret Manager..."
for SECRET in GEMINI_API_KEY SECRET_KEY; do
  if ! gcloud secrets describe "${SECRET}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "ERROR: Secret '${SECRET}' not found in Secret Manager."
    echo "Create it with: echo -n 'your-value' | gcloud secrets create ${SECRET} --data-file=- --project=${PROJECT_ID}"
    exit 1
  fi
  echo "  Found: ${SECRET}"
done

# ── Step 3: Build container image ─────────────────────────────────
echo "[3/5] Building container image via Cloud Build..."
gcloud builds submit \
  --tag "${IMAGE}" \
  --project="${PROJECT_ID}" \
  --quiet

# ── Step 4: Deploy to Cloud Run ───────────────────────────────────
echo "[4/5] Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}" \
  --platform managed \
  --region "${REGION}" \
  --project="${PROJECT_ID}" \
  --min-instances 1 \
  --max-instances 10 \
  --memory 2Gi \
  --timeout 300 \
  --set-env-vars "APP_MODE=PROD,E2E_MODE=0,LLM_PROVIDER=GEMINI" \
  --set-secrets "GEMINI_API_KEY=GEMINI_API_KEY:latest,SECRET_KEY=SECRET_KEY:latest" \
  --session-affinity \
  --allow-unauthenticated \
  --quiet

# ── Step 5: Verify deployment ─────────────────────────────────────
echo "[5/5] Verifying deployment..."
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
  --region "${REGION}" \
  --project="${PROJECT_ID}" \
  --format='value(status.url)')

echo ""
echo "=== Deployment Complete ==="
echo "  URL: ${SERVICE_URL}"
echo ""

# Health check
echo "Running health check..."
HEALTH=$(curl -sf "${SERVICE_URL}/healthz" 2>/dev/null || echo '{"status":"unreachable"}')
echo "  Response: ${HEALTH}"
echo ""
echo "Next steps:"
echo "  - Dashboard:  ${SERVICE_URL}"
echo "  - Voice demo: ${SERVICE_URL}/live-voice"
echo "  - API docs:   ${SERVICE_URL}/docs"
