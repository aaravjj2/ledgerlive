# LedgerLive — Finance Ops Close Agent

> Automated finance close workflow: document ingestion → OCR/extraction →
> reconciliation → exception triage → HITL review → evidence binder → audit trail.

## Project Identity

```
PROJECT_ID: LEDGERLIVE
```

## Quick Start

```bash
# Backend
cd apps/api
.venv/Scripts/python -m uvicorn app.main:app --port 8090 --reload

# Frontend
cd apps/web
npm run dev

# Tests
cd apps/api && .venv/Scripts/python -m pytest tests/ -v
```

## Architecture

| Layer | Tech | Port |
|-------|------|------|
| API | FastAPI + Python 3.14 | 8090 |
| Web | React 18 + Vite + Tailwind | 5173 (dev) / 4173 (preview) |
| DB | SQLite (local) | — |
| E2E | Playwright MCP headed-only | — |

## Gates

- `tools/gates/no_apex_references.py` — Zero Apex Terminal references
- `tools/gates/no_network_in_tests.py` — No outbound network in tests
