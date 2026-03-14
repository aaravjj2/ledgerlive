# LedgerLive -- Airia Hackathon Judging Guide

> Estimated judge spin-up time: **under 5 minutes**.

---

## Prerequisites

- Git, Python 3.11+, Node.js 18+
- No external API keys required (DEMO mode uses mock inference)
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
# Default .env works out of the box for DEMO mode

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

### 2. Airia Integration Endpoints (start here)

```bash
# MCP Tools -- 8 registered tools callable from Airia
curl http://localhost:8090/api/mcp/tools | python3 -m json.tool

# Airia Compatibility Report -- 10 checks, all PASS
curl http://localhost:8090/api/airia/compat_report | python3 -m json.tool

# Airia Webhook Delivery Log -- evidence of webhook processing
curl http://localhost:8090/api/airia/webhook_log | python3 -m json.tool

# Airia Bundle Manifest -- community listing metadata
curl http://localhost:8090/api/airia/bundle | python3 -m json.tool

# Blueprint Builder -- no-code workflow definitions
curl http://localhost:8090/api/blueprint/list | python3 -m json.tool
```

### 3. Four-Agent Pipeline Endpoints

```bash
# IngestionAgent -- document intake
curl http://localhost:8090/api/documents | python3 -m json.tool

# ReconciliationAgent -- matching results
curl http://localhost:8090/api/reconciliations | python3 -m json.tool

# ExceptionTriageAgent -- AI-classified exceptions
curl http://localhost:8090/api/exceptions | python3 -m json.tool

# HITLCoordinatorAgent -- review queue with approval context
curl http://localhost:8090/api/review-queue | python3 -m json.tool

# Full workflow with reasoning trace
curl http://localhost:8090/api/workflows | python3 -m json.tool
```

### 4. Airia-Specific Verification

```bash
# Run the Airia compatibility suite
make airia:compat
# Expected: 10/10 checks PASS

# Generate and validate the community listing bundle
make airia:bundle
make airia:validate
# Expected: bundle.json generated and valid

# Run the full test suite
cd apps/api && python3 -m pytest tests/ -v --tb=short
# Expected: 4,269+ tests passing
```

### 5. Frontend Walkthrough

Open **http://localhost:4173** and verify:

| Page | What to look for |
|------|-----------------|
| Dashboard | All four agent stages visible with real-time progress |
| Documents | IngestionAgent output: uploaded docs with hashes |
| Reconciliations | ReconciliationAgent output: match scores and explanations |
| Exceptions | ExceptionTriageAgent output: severity, confidence, classification |
| Review Queue | HITLCoordinatorAgent output: approval context, reasoning chain |
| Race Control | Orchestration view: lanes per agent, scoreboard, live status |
| Airia Readiness | MCP tools, compatibility report, webhook log, bundle export |
| Evidence Binder | Court-ready pack with SHA-256 seal and full decision lineage |

---

## What to Evaluate

| Criterion | Where to find evidence |
|-----------|----------------------|
| **Airia integration depth** | 8 MCP tools, webhook delivery, community listing bundle, no-code builder |
| **Multi-agent architecture** | 4 specialized agents with nested sub-agent invocation |
| **HITL design** | Dynamic document generation with full upstream reasoning chain |
| **Cross-system integration** | Google Drive, Slack, QuickBooks mock, email ingestion |
| **Audit readiness** | SHA-256 sealed evidence binders, complete decision lineage |
| **Test coverage** | 4,269 tests including Airia-specific compatibility tests |

---

## Key Differentiators for Airia Judges

1. **Not just tool registration** -- The 8 MCP tools are actively used by the agent pipeline, not just declared. Each tool call is logged with input, output, and latency.

2. **Nested agent architecture** -- The ExceptionTriageAgent spawns sub-agents for specialized investigation. This is visible in the workflow reasoning traces.

3. **Dynamic HITL documents** -- The HITLCoordinatorAgent generates approval documents that include the full decision chain from all upstream agents. Reviewers see context, not just a checkbox.

4. **Deterministic verification** -- Running the same close twice produces identical results. The `make airia:compat` check verifies deterministic checksums.

5. **Community listing ready** -- `make airia:bundle` produces a deployable community listing artifact.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8090 in use | `lsof -i :8090` and kill the process |
| `ModuleNotFoundError` | Activate the venv: `source apps/api/.venv/bin/activate` |
| `make airia:compat` fails | Ensure the API is running on port 8090 first |
| Docker build fails | Run `docker compose down -v` first, then rebuild |
| Webhook test fails | Webhook log requires the API to have been running for >10 seconds (seed data loads at startup) |
