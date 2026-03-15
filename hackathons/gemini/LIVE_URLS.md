# LedgerLive — Live Deployment URLs (Gemini Hackathon)

Deployed: 2026-03-15 (UI redesign + new revision)

## Backend API (Cloud Run)
- URL: https://ledgerlive-api-zkw2sk4rha-uc.a.run.app
- Docs: https://ledgerlive-api-zkw2sk4rha-uc.a.run.app/docs
- OpenAPI JSON: https://ledgerlive-api-zkw2sk4rha-uc.a.run.app/openapi.json
- Voice Status: https://ledgerlive-api-zkw2sk4rha-uc.a.run.app/api/voice/status
- Voice WebSocket: wss://ledgerlive-api-zkw2sk4rha-uc.a.run.app/ws/voice

## Frontend (Cloud Run)
- URL: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app
- Race Control: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/race-control
- Live Voice Agent: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/live-voice
- Documents: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/documents
- Reconciliation: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/reconciliation
- Audit Log: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/audit
- Review Queue: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/review
- Exceptions: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app/exceptions

## Google Cloud Project
- Project ID: gen-lang-client-0432346640
- Account: ajtopper2412@gmail.com
- Region: us-central1
- Services: ledgerlive-api (2 vCPU, 2 GiB), ledgerlive-web (1 vCPU, 512 MiB)
- Notes: Cloud Run revisions — api@00004-2q2, web@00005-bzq (2026-03-15, F1 dark UI deployed)

## Gemini API Integration
- genai_available: true
- api_key_configured: true
- model: gemini-2.0-flash (Live API)
- features: voice WebSocket, tool calling (8 finance tools), session management

## Proof
- Cloud Run JSON: hackathons/gemini/cloud-run-service.json
- Deployment list: hackathons/gemini/proof-of-deployment.txt
- Deployment timestamp: 2026-03-15T04:38:03Z

## New UI Screenshots (2026-03-15 — F1 Dark Redesign — 10/10)
- [PASS] NEW-01-dashboard — artifacts/demo/NEW-01-dashboard.png
- [PASS] NEW-02-race-control — artifacts/demo/NEW-02-race-control.png
- [PASS] NEW-03-exceptions — artifacts/demo/NEW-03-exceptions.png
- [PASS] NEW-04-reconciliation — artifacts/demo/NEW-04-reconciliation.png
- [PASS] NEW-05-live-voice — artifacts/demo/NEW-05-live-voice.png
- [PASS] NEW-06-audit — artifacts/demo/NEW-06-audit.png
- [PASS] NEW-07-sidebar — artifacts/demo/NEW-07-sidebar.png
- [PASS] NEW-03-dashboard-seeded — artifacts/demo/NEW-03-dashboard-seeded.png
- [PASS] NEW-08-race-control-seeded — artifacts/demo/NEW-08-race-control-seeded.png
- [PASS] NEW-09-exceptions-seeded — artifacts/demo/NEW-09-exceptions-seeded.png


## Smoke Test Results (2026-03-14 — Updated)
- [PASS] /api/documents (200)
- [PASS] /api/reconciliations (200)
- [PASS] /api/exceptions (200)
- [PASS] /api/audit (200)
- [PASS] /api/race-control (200)
- [PASS] /api/voice/status → genai_available:true, api_key_configured:true
- [PASS] /docs (200)
- [PASS] /openapi.json (200)
- [PASS] Frontend / (200)
- [PASS] Frontend /race-control (200)
- [PASS] Frontend /documents (200)
- [PASS] Frontend /reconciliation (200) [fixed from /reconciliations]
- [PASS] Frontend /review (200)
- [PASS] Frontend /audit (200)
- [PASS] Frontend /live-voice (200)
- [PASS] WebSocket wss://.../ws/voice → LedgerBot greeting received

## Voice API Tests (2026-03-14)
- [PASS] POST /api/voice/ask "Show me open exceptions" → 89ms smart response
- [PASS] POST /api/voice/ask "Reconciliation status?" → 78ms smart response
- [PASS] POST /api/voice/ask "Close cycle status?" → 80ms smart response
- [PASS] POST /api/voice/ask "Approve low-risk exceptions?" → 87ms smart response

## Page Screenshot Results (2026-03-14 — 8/8)
- [PASS] 01-dashboard — artifacts/demo/01-dashboard.png
- [PASS] 02-race-control — artifacts/demo/02-race-control.png
- [PASS] 03-documents — artifacts/demo/03-documents.png
- [PASS] 04-reconciliation — artifacts/demo/04-reconciliation.png
- [PASS] 05-exceptions — artifacts/demo/05-exceptions.png
- [PASS] 06-review — artifacts/demo/06-review.png
- [PASS] 07-audit — artifacts/demo/07-audit.png
- [PASS] 08-voice — artifacts/demo/08-voice.png
