# LedgerLive Demo — Race Day Walkthrough

> **3-minute scripted demo** for Airia "Race Beyond the Track" — Williams F1 / Atlassian hackathon.

---

## Setup (30 seconds)

```bash
# Clone & start
git clone https://github.com/aaravjj2/ledgerlive.git
cd ledgerlive
cp .env.example .env
make demo
# → API on :8090, Frontend preview on :4173
```

Open **http://127.0.0.1:4173** in your browser.

---

## Race Day Walkthrough (10 steps)

### 🏁 Step 1 — Dashboard (Pit Lane Overview)
Navigate to the **Dashboard**. This is your Pit Lane — a single view of every close cycle metric: documents ingested, OCR pipeline status, reconciliation progress, open exceptions, and workflow stage.

### 📄 Step 2 — Pit Stop: Document Ingestion
Click **Documents**. Upload an invoice PDF. The agent ingests it, computes a content hash, and queues it for OCR — like the pit crew prepping tires before a stop.

### 🔍 Step 3 — Qualifying Lap: OCR Pipeline
Navigate to **OCR Jobs**. Watch the pipeline extract text from documents with >94% confidence. Each job shows status, extracted text, and model confidence — this is your qualifying lap data.

### 🔄 Step 4 — Race Start: Reconciliation
Open **Reconciliations**. The agent runs bank-to-GL, subledger-to-GL, and vendor statement reconciliations. Each shows match score, explanation, and AI reasoning trace — not just "matched/unmatched".

### ⚠️ Step 5 — Safety Car: Exception Triage
Navigate to **Exceptions**. The AI triages each mismatch with severity, confidence score, and classification (auto-resolvable vs. requires-approval). Critical items like duplicate payments trigger a Safety Car — the close process pauses until resolved.

### 👤 Step 6 — Human-in-the-Loop Review
Open the **Review Queue**. High-severity exceptions are routed to the right approver. Each item shows the AI's reasoning for why it was escalated — not a black box.

### 🏎️ Step 7 — Race Control Dashboard
Navigate to **Race Control** (`/api/race-control`). This is the live command center: lanes for each close stage, a scoreboard, and real-time progress. Think of it as your F1 race engineer's screen.

### 📦 Step 8 — Evidence Binder (Court Pack)
Click **Evidence Binder**. The agent compiles all documents, reconciliation results, exception resolutions, and approval chains into a tamper-evident, SHA-256 sealed court pack — ready for audit.

### 🤖 Step 9 — Airia MCP Gateway
Navigate to the **Airia Readiness** page. View the 8 MCP tools exposed for Airia integration, the compatibility report (10 checks PASS), and export the MCP Gateway config for one-click Airia deployment.

### 🏆 Step 10 — Replay & Telemetry
Review the **Workflow** with full reasoning trace. The agent explains every decision: why it auto-resolved timing differences, why it escalated duplicates, and what it would do next. This is your race telemetry — every lap documented.

---

## Key Demo Talking Points

- **Autonomy**: The agent doesn't just label — it decides. Auto-resolves low-severity exceptions, escalates critical ones with reasoning.
- **F1 Metaphor**: Every close stage maps to an F1 race phase. Pit stops = ingestion, qualifying = reconciliation, safety car = exceptions, podium = sign-off.
- **Airia Integration**: 8 MCP tools, webhook delivery log, Airia-compatible config export. Not just "mentioned in README" — actually callable.
- **Audit-Ready**: Every mutation logged, every decision explained, every artifact sealed with SHA-256.

---

## API Endpoints for Live Demo

| Endpoint | What it proves |
|----------|---------------|
| `GET /api/race-control` | Live Race Control state with lanes, scoreboard, reasoning |
| `GET /api/documents` | Real documents in the system |
| `GET /api/ocr-jobs/stats` | OCR pipeline has actually run (completed > 0) |
| `GET /api/reconciliations` | Reconciliation results with explanations |
| `GET /api/exceptions` | AI-triaged exceptions with confidence scores |
| `GET /api/workflows` | Workflow with reasoning trace |
| `GET /api/mcp/tools` | 8 MCP tools for Airia |
| `GET /api/airia/compat_report` | 10-check Airia compatibility |
| `GET /api/airia/webhook_log` | Webhook delivery evidence |
