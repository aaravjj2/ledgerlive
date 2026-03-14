# LedgerLive -- DigitalOcean Hackathon Judging Guide

> Estimated judge spin-up time: **under 5 minutes**.

---

## Prerequisites

- Git, Python 3.11+, Node.js 18+
- (Optional) A DigitalOcean account with Gradient AI access for live inference
- (Optional) Docker and Docker Compose

---

## Option A: Local Quick Start (recommended)

```bash
# 1. Clone
git clone https://github.com/aaravjj2/ledgerlive.git
cd ledgerlive
git checkout waves

# 2. Configure
cp .env.example .env
# Edit .env and set:
#   LLM_PROVIDER=DEMO          (runs without external API keys)
#   APP_MODE=DEMO

# For live Gradient AI inference, also set:
#   GRADIENT_AI_API_KEY=your-key-here
#   LLM_PROVIDER=GRADIENT

# 3. Install backend
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd ../..

# 4. Install frontend
cd apps/web && npm install && cd ../..

# 5. Launch
make demo
# API on http://localhost:8090
# Frontend on http://localhost:4173
```

## Option B: Docker Compose

```bash
git clone https://github.com/aaravjj2/ledgerlive.git
cd ledgerlive && git checkout waves
cp .env.example .env
# Edit .env as above
docker compose up --build
# API on :8090, Frontend on :3000
```

---

## Verification Checklist

### 1. Health Check

```bash
curl http://localhost:8090/healthz
```

Expected:
```json
{
  "project": "LEDGERLIVE",
  "status": "ok",
  "mode": "DEMO",
  "llm": "DEMO",
  "ts": "2026-03-13T..."
}
```

### 2. Core Finance Agent Endpoints

```bash
# Documents -- ingestion pipeline
curl http://localhost:8090/api/documents | python3 -m json.tool

# OCR pipeline -- extraction results with confidence scores
curl http://localhost:8090/api/ocr-jobs/stats | python3 -m json.tool

# Reconciliation -- bank-to-GL matches with AI reasoning
curl http://localhost:8090/api/reconciliations | python3 -m json.tool

# Exceptions -- AI-triaged with severity and classification
curl http://localhost:8090/api/exceptions | python3 -m json.tool

# Evidence binder -- SHA-256 sealed audit artifact
curl http://localhost:8090/api/evidence-binder | python3 -m json.tool

# Race Control -- live close progress dashboard
curl http://localhost:8090/api/race-control | python3 -m json.tool
```

### 3. Gradient AI Integration Points

```bash
# OCR pipeline uses Gradient AI for extraction
curl http://localhost:8090/api/ocr-jobs/stats | python3 -m json.tool
# Look for: confidence scores, extraction status, field counts

# Gradient adapter endpoint
curl http://localhost:8090/api/gradient/status | python3 -m json.tool

# ML inference pipeline
curl http://localhost:8090/api/ml/inference | python3 -m json.tool
```

### 4. Test Suite

```bash
cd apps/api
python3 -m pytest tests/ -v --tb=short
# Expected: 4,269+ tests passing
```

### 5. Frontend Walkthrough

Open **http://localhost:4173** and verify:

| Page | What to look for |
|------|-----------------|
| Dashboard | Close cycle overview with all pipeline stages |
| Documents | Upload a PDF; watch ingestion and hash computation |
| OCR Jobs | Extraction results with per-field confidence scores |
| Reconciliations | Bank-to-GL matches with AI explanations |
| Exceptions | Severity classification, auto-resolve vs. escalate |
| Race Control | Live lanes per close stage, scoreboard |
| Evidence Binder | Court-ready pack with SHA-256 seal |

---

## What to Evaluate

| Criterion | Where to find evidence |
|-----------|----------------------|
| **DigitalOcean usage** | Architecture uses App Platform, Gradient AI, Managed Postgres, Spaces |
| **Gradient AI integration** | OCR extraction pipeline, field classification, confidence scoring |
| **Technical depth** | 4,269 tests; 340 endpoints; nested agent architecture with reasoning traces |
| **Best AI Agent Persona** | LedgerBot F1 persona: racing commentary in every API response and dashboard view |
| **Best Program for the People** | Small Business Mode: simplified terminology, guided walkthroughs, 30-min close |

---

## Special Prize Evidence

### Best AI Agent Persona -- LedgerBot

- Navigate to **Race Control** (`/api/race-control`) -- observe the F1 racing metaphor across lanes, stages, and commentary
- Check API responses for reasoning traces that use racing terminology
- Review the DEMO walkthrough in the root `DEMO.md` for the full persona narrative

### Best Program for the People -- Small Business Mode

- Set `APP_MODE=SMALL_BIZ` in `.env` and restart
- Observe simplified terminology and reduced approval steps
- First-time user guided walkthrough activates automatically

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8090 in use | `lsof -i :8090` and kill the process |
| `ModuleNotFoundError` | Ensure you activated the venv: `source apps/api/.venv/bin/activate` |
| Docker build fails | Run `docker compose down -v` first, then rebuild |
| Frontend shows blank page | Check that the API is running on 8090; the frontend proxies to it |
| Gradient AI timeout | The DEMO mode uses mock inference; set `LLM_PROVIDER=DEMO` to bypass |
