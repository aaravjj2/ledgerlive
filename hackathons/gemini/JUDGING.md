# LedgerLive -- Gemini Hackathon Judging Guide

> Estimated judge spin-up time: **under 5 minutes**.

---

## Prerequisites

- Git, Python 3.11+, Node.js 18+
- A Gemini API key ([aistudio.google.com/apikey](https://aistudio.google.com/apikey))
- (Optional) Docker and Docker Compose for one-command startup

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
#   GEMINI_API_KEY=your-key-here
#   LLM_PROVIDER=GEMINI

# 3. Install backend
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd ../..

# 4. Install frontend
cd apps/web && npm install && cd ../..

# 5. Launch
make demo
# API starts on http://localhost:8090
# Frontend starts on http://localhost:4173
```

## Option B: Docker Compose

```bash
git clone https://github.com/aaravjj2/ledgerlive.git
cd ledgerlive && git checkout waves
cp .env.example .env
# Edit .env: set GEMINI_API_KEY and LLM_PROVIDER=GEMINI
docker compose up --build
# API on :8090, Frontend on :3000
```

## Option C: Google Cloud Run (deployed)

If a live deployment URL is provided in the submission, visit it directly. No local setup required.

---

## Verification Checklist

Run these in order to validate the submission:

### 1. Health Check

```bash
curl http://localhost:8090/healthz
```

Expected response:
```json
{
  "project": "LEDGERLIVE",
  "status": "ok",
  "mode": "DEMO",
  "llm": "GEMINI",
  "ts": "2026-03-13T..."
}
```

Confirm `"llm": "GEMINI"` appears in the response.

### 2. API Endpoints (core finance agent)

```bash
# Race Control dashboard state
curl http://localhost:8090/api/race-control | python3 -m json.tool

# Reconciliation results with AI explanations
curl http://localhost:8090/api/reconciliations | python3 -m json.tool

# AI-triaged exceptions with confidence scores
curl http://localhost:8090/api/exceptions | python3 -m json.tool

# Evidence binder (audit-ready, SHA-256 sealed)
curl http://localhost:8090/api/evidence-binder | python3 -m json.tool

# MCP tools registry (8 tools)
curl http://localhost:8090/api/mcp/tools | python3 -m json.tool
```

### 3. Voice Interface (Gemini Live API)

1. Open **http://localhost:4173/live-voice** in Chrome (microphone access required).
2. Click the microphone button to start a session.
3. Say: *"What is the current close status?"*
4. The agent should respond with audio describing the close cycle progress.
5. Try an interruption: start speaking while the agent is responding -- it should stop and listen.

### 4. Test Suite

```bash
cd apps/api
python3 -m pytest tests/ -v --tb=short
# Expected: 4,269+ tests passing
```

### 5. Frontend Walkthrough

Open **http://localhost:4173** and navigate through:

| Page | What to look for |
|------|-----------------|
| Dashboard | Pit Lane overview: documents, OCR status, reconciliation progress |
| Documents | Upload an invoice PDF; observe ingestion and hash computation |
| OCR Jobs | Pipeline status with >94% confidence scores |
| Reconciliations | Bank-to-GL matches with AI reasoning traces |
| Exceptions | Severity classification, confidence scores, auto-resolve vs. escalate |
| Race Control | Live lanes for each close stage, scoreboard, progress |
| Evidence Binder | Tamper-evident court pack with SHA-256 seal |

---

## What to Evaluate

| Criterion | Where to find evidence |
|-----------|----------------------|
| **Gemini API usage** | Live voice at `/live-voice`; tool calling in WebSocket logs; multimodal doc input |
| **Google Cloud integration** | `hackathons/gemini/deploy.sh` for Cloud Run, Artifact Registry, Secret Manager |
| **Technical depth** | 4,269 tests; 340 API endpoints; nested agent architecture |
| **Creativity** | F1 racing metaphor maps close stages to race phases (pit stop, safety car, checkered flag) |
| **Impact** | Hands-free exception review; 3x faster approvals; audit-ready evidence binders |

---

## Deployment Script

See `hackathons/gemini/deploy.sh` for the full Cloud Run deployment automation.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `GEMINI_API_KEY not set` | Ensure `.env` contains a valid key from [aistudio.google.com](https://aistudio.google.com/apikey) |
| Port 8090 in use | `lsof -i :8090` and kill the process, or set `API_PORT=8091` in `.env` |
| Voice not working | Use Chrome (WebAudio API required); grant microphone permission |
| Docker build fails | Ensure Docker Desktop is running; try `docker compose down -v` first |
| Tests fail on import | Run `pip install -r requirements.txt` inside the virtual environment |
