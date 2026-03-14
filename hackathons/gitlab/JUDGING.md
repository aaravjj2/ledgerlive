# LedgerLive -- GitLab AI Hackathon Judging Guide

> Estimated judge spin-up time: **under 5 minutes**.

---

## Prerequisites

- Git, Python 3.11+, Node.js 18+
- No external API keys required for local evaluation (DEMO mode uses mock inference)
- (Optional) Anthropic API key for live Claude compliance analysis
- (Optional) GitLab personal access token for MR integration demo
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
# Default .env works for DEMO mode

# For live Claude compliance analysis, also set:
#   ANTHROPIC_API_KEY=your-key-here
# For GitLab MR integration:
#   GITLAB_TOKEN=your-token-here

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

### 2. Compliance and Controls Endpoints

```bash
# Controls catalog -- SOX, SOC 2, GDPR controls
curl http://localhost:8090/api/controls | python3 -m json.tool

# Compliance bundle -- full compliance posture
curl http://localhost:8090/api/compliance-bundle | python3 -m json.tool

# SOC 2 evidence
curl http://localhost:8090/api/soc2/evidence | python3 -m json.tool

# Audit integrity -- tamper detection
curl http://localhost:8090/api/audit-integrity | python3 -m json.tool

# Security posture pack
curl http://localhost:8090/api/security/posture-pack | python3 -m json.tool
```

### 3. GitLab Duo Agent Endpoints

```bash
# Compliance signing -- MR annotation simulation
curl http://localhost:8090/api/compliance/signing | python3 -m json.tool

# Policy engine -- rule evaluation
curl http://localhost:8090/api/policy/engine | python3 -m json.tool

# Breaking change detection
curl http://localhost:8090/api/breaking-change/detect | python3 -m json.tool

# Tool scope matrix -- what each agent tier can access
curl http://localhost:8090/api/security/tool-scope-matrix | python3 -m json.tool
```

### 4. Green Agent Tiered Inference

```bash
# Model governance -- which model tier is used per risk level
curl http://localhost:8090/api/ml/governance | python3 -m json.tool

# ML impact assessment -- energy savings data
curl http://localhost:8090/api/ml/impact | python3 -m json.tool

# Productivity ROI -- efficiency metrics
curl http://localhost:8090/api/telemetry/productivity-roi | python3 -m json.tool
```

### 5. Test Suite

```bash
cd apps/api
python3 -m pytest tests/ -v --tb=short
# Expected: 4,269+ tests passing

# Compliance-specific tests:
python3 -m pytest tests/test_w37_controls_catalog.py tests/test_w101_soc2_evidence.py tests/test_w106_compliance_signing.py -v
```

### 6. Frontend Walkthrough

Open **http://localhost:4173** and verify:

| Page | What to look for |
|------|-----------------|
| Dashboard | Close cycle overview with compliance status indicators |
| Controls | Full controls catalog (SOX, SOC 2, GDPR) |
| Compliance Bundle | Aggregated compliance posture across all controls |
| Audit Portal | Audit trail with tamper detection badges |
| Evidence Binder | Court-ready pack with SHA-256 seal |
| Race Control | Live lanes showing compliance gate status |

---

## What to Evaluate

### Main Prize

| Criterion | Where to find evidence |
|-----------|----------------------|
| **GitLab Duo Agent** | Compliance analysis endpoints, MR annotation simulation, policy engine |
| **Technical depth** | 4,269 tests; 340 endpoints; controls catalog with SOX/SOC2/GDPR mapping |
| **Real-world utility** | Pre-merge compliance detection prevents audit findings |
| **Agent design** | Tiered risk classification drives different analysis depths |

### Bonus: Anthropic Integration ($13,500)

| Evidence | Location |
|----------|----------|
| Claude for semantic diff analysis | `/api/compliance/signing` -- compliance reasoning in MR annotations |
| Claude for control mapping | `/api/policy/engine` -- maps changes to affected controls |
| Claude for risk classification | LOW/MEDIUM/HIGH/CRITICAL risk tiers with model-generated rationale |
| Impact narrative generation | Human-readable compliance summaries in MR comment format |

### Bonus: Google Cloud Integration ($13,500)

| Evidence | Location |
|----------|----------|
| Cloud Function agent runner | `hackathons/gitlab/description.md` -- architecture section |
| Secret Manager for API keys | `.env.example` shows secret references; deploy script uses Secret Manager |
| Cloud Logging integration | Audit log endpoints with structured logging format |

### Bonus: Green Agent ($3,000)

| Evidence | Location |
|----------|----------|
| Tiered inference by risk level | `/api/ml/governance` -- shows model selection per risk tier |
| Energy savings quantification | `/api/ml/impact` -- estimated 60-75% reduction |
| No-LLM path for low-risk | Pattern matching handles comments, formatting, trivial changes |
| Haiku for medium risk | Lightweight model for standard config changes |
| Sonnet for high/critical risk | Full analysis reserved for compliance-critical changes |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8090 in use | `lsof -i :8090` and kill the process |
| `ModuleNotFoundError` | Activate the venv: `source apps/api/.venv/bin/activate` |
| Compliance endpoints return empty | Ensure `APP_MODE=DEMO` and `E2E_MODE=1` are set in `.env` |
| Docker build fails | Run `docker compose down -v` first, then rebuild |
| GitLab integration not connecting | The DEMO mode simulates GitLab MR events; set `GITLAB_TOKEN` for live integration |
