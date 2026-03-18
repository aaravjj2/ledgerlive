# LedgerLive — Live Deployment URLs

## Cloud Run Services

| Service  | URL |
|----------|-----|
| Frontend | https://ledgerlive-web-570445019871.us-central1.run.app |
| Backend  | https://ledgerlive-api-production.up.railway.app |

## Current Revisions (2026-03-15)

| Service       | Revision              | Notes |
|---------------|-----------------------|-------|
| ledgerlive-web | `web-00006-gcp`      | Sidebar layout + F1 dark theme |
| ledgerlive-api | `api-00004-2q2`      | FastAPI + Gemini Live |

## Health Checks

- Frontend: `https://ledgerlive-web-570445019871.us-central1.run.app` → HTTP 200
- Backend: `https://ledgerlive-api-production.up.railway.app/api/exceptions` → HTTP 200

## Key Pages

| Page | URL |
|------|-----|
| Dashboard (Pit Lane) | `/` |
| Multi-Agent Orchestrator | `/multi-agent` |
| CFO Cockpit | `/cfo-cockpit` |
| Gradient AI | `/gradient-ai` |
| HackathonShowcase | `/showcase` |
| LedgerBot Voice | `/live-voice` |
| Audit Log | `/audit` |
| Evidence Binder | `/evidence-binder` |
| Close Calendar | `/close-calendar` |

## Screenshots (artifacts/demo/)

15 FINAL screenshots with sidebar layout captured 2026-03-15:
- FINAL-01-dashboard.png — Pit Lane command center
- FINAL-02-race-control.png — Race Control
- FINAL-03-cfo-cockpit.png — CFO Cockpit KPIs
- FINAL-04-evidence-binder.png — SHA-256 hash binder
- FINAL-05-multi-agent.png — 5-agent pipeline
- FINAL-06-close-calendar.png — Close Calendar
- FINAL-07-audit-log.png — Timeline audit log
- FINAL-08-board-pack.png — Board pack accordion
- FINAL-09-gradient-ai.png — OCR + training jobs
- FINAL-10-connectors.png — Integration marketplace
- FINAL-11-bloomberg.png — Bloomberg terminal
- FINAL-12-hackathon.png — Hackathon showcase
- FINAL-13-exceptions.png — Exceptions triage
- FINAL-14-documents.png — Document ingestion
- FINAL-15-live-voice.png — LedgerBot voice UI
