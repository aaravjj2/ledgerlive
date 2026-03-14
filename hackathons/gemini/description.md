# LedgerLive -- Voice-Enabled Finance Close Agent

## The Problem

Finance teams at mid-market companies spend 40+ hours per quarter on the manual close process. Controllers toggle between spreadsheets, ERPs, bank portals, and Slack threads -- copy-pasting numbers, chasing approvals, and documenting every decision for auditors. The work is high-stakes (material misstatements carry legal consequences) but mechanically repetitive: reconcile accounts, triage exceptions, route approvals, compile evidence binders. Hands are occupied. Eyes are locked on screens. The phone rings, and the close falls behind.

Current automation tools digitize the spreadsheet but do not eliminate the spreadsheet. Accountants still click through the same workflows, one field at a time.

## The Solution

LedgerLive is a voice-enabled finance close agent powered by the **Gemini 2.0 Flash Live API**. Instead of clicking through a dashboard, the controller speaks:

> "Show me all open exceptions over ten thousand dollars for the APAC entity."

The agent responds with real-time audio, reads back the three open items, and asks whether to auto-resolve the timing differences or escalate the duplicate payment to the CFO. The controller approves by voice while walking to a meeting. The close moves forward.

## How Gemini Is Used

LedgerLive integrates Gemini at three layers:

1. **Gemini Live API (audio-in / audio-out)** -- The `/api/gemini/live-voice` WebSocket endpoint streams bidirectional audio using `gemini-2.0-flash-live`. The model handles turn-taking, interruption detection, and natural conversation flow. When the controller interrupts mid-sentence ("wait, skip that one"), the agent stops and adjusts immediately.

2. **Gemini tool calling for database queries** -- The Live API session is configured with function declarations that map to LedgerLive's internal tools: `query_exceptions`, `approve_item`, `run_reconciliation`, `get_close_status`. Gemini decides which tool to invoke based on the spoken request, executes the query against the live database, and narrates the result back as audio.

3. **Gemini for document understanding** -- Uploaded invoices and bank statements pass through Gemini's multimodal input for field extraction and classification before entering the reconciliation pipeline. Confidence scores are attached to every extracted value.

## Google Cloud Services

| Service | Role |
|---------|------|
| **Cloud Run** | Hosts the FastAPI backend with session affinity for WebSocket connections. Min 1 / max 10 instances, 2 GiB memory, 300s timeout. |
| **Artifact Registry** | Stores container images built via `gcloud builds submit`. |
| **Secret Manager** | Manages `GEMINI_API_KEY` and `SECRET_KEY` -- never stored in environment variables or source. |
| **Cloud Build** | CI/CD pipeline triggers on push to the `waves` branch, runs 4,269 pytest tests, and deploys to Cloud Run on green. |

## Target Users

- **CFOs** who review close status across entities during back-to-back meetings and need hands-free updates
- **Controllers** who run the close and spend hours clicking through exception queues that could be triaged by voice
- **Accounting Managers** who coordinate across teams and need real-time status without opening a laptop

## Impact

- **Hands-free exception review**: Controllers triage exceptions by voice while reviewing physical documents, reducing context-switch overhead by an estimated 60%.
- **3x faster approval cycle**: Voice approvals eliminate the queue-check-click-confirm loop. An approval that takes 90 seconds in a dashboard takes 10 seconds by voice.
- **Audit-ready by default**: Every voice interaction is logged with a transcript, tool call trace, and SHA-256 sealed evidence binder. Auditors get the reasoning, not just the result.
- **4,269 passing tests**: The agent is not a prototype. The full test suite (pytest + Playwright E2E) passes on every commit.

## Repository

- **GitHub**: [github.com/aaravjj2/ledgerlive](https://github.com/aaravjj2/ledgerlive)
- **Branch**: `waves`
- **Quick start**: `git clone && cp .env.example .env && make demo`
- **Voice demo**: `http://localhost:4173/live-voice`
