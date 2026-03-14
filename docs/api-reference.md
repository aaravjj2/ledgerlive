# LedgerLive API Reference

> Base URL: `http://localhost:8090`
>
> All endpoints return JSON. Pagination uses `?limit=N` query parameters.

---

## Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/healthz` | Liveness probe. Returns project ID, mode, LLM provider, and timestamp. |
| `GET` | `/api/health/dashboard` | Aggregated health across all service waves. |

```json
// GET /healthz
{
  "project": "LEDGERLIVE",
  "status": "ok",
  "mode": "DEMO",
  "llm": "DEMO",
  "ts": "2026-03-13T12:00:00"
}
```

---

## Close Periods

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/close-periods` | List all close periods. |
| `POST` | `/api/close-periods` | Create a new close period. |
| `GET` | `/api/close-periods/{id}` | Get period details. |
| `POST` | `/api/close-periods/{id}/close` | Finalize and close a period. |

```json
// GET /api/close-periods
{
  "items": [
    { "period_id": "uuid", "name": "Q1 2026", "status": "open", "start_date": "2026-01-01", "end_date": "2026-03-31" }
  ],
  "total": 1
}
```

---

## Entities

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/entities` | List legal entities. |
| `POST` | `/api/entities` | Register a new entity. |
| `GET` | `/api/entities/{id}` | Get entity details. |

```json
// GET /api/entities
{ "items": [{ "entity_id": "uuid", "name": "Acme Corp", "currency": "USD" }], "total": 1 }
```

---

## Documents

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/documents` | List ingested documents. |
| `POST` | `/api/documents` | Upload and register a document. Content-hash is computed on ingest. |
| `GET` | `/api/documents/{id}` | Get document metadata and content hash. |

```json
// GET /api/documents
{
  "items": [{ "document_id": "uuid", "filename": "invoice_001.pdf", "content_hash": "a1b2c3...", "status": "processed" }],
  "total": 1
}
```

---

## OCR Pipeline

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/ocr-jobs` | List OCR processing jobs. |
| `POST` | `/api/ocr-jobs` | Submit a document for OCR extraction. |
| `GET` | `/api/ocr-jobs/{id}` | Get OCR job result including extracted text and confidence. |
| `GET` | `/api/ocr-jobs/stats` | Pipeline statistics (completed, pending, avg confidence). |

```json
// GET /api/ocr-jobs/stats
{ "total": 5, "completed": 4, "pending": 1, "avg_confidence": 0.94 }
```

---

## Reconciliation

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/reconciliations` | List reconciliation runs with match scores. |
| `POST` | `/api/reconciliations` | Start a new reconciliation run. |
| `GET` | `/api/reconciliations/{id}` | Get reconciliation details including explanation. |
| `POST` | `/api/reconciliations/{id}/approve` | Approve a reconciliation match. |
| `POST` | `/api/reconciliations/{id}/reject` | Reject a reconciliation match. |

```json
// GET /api/reconciliations
{
  "items": [{
    "recon_id": "uuid",
    "source_type": "bank_statement",
    "target_type": "general_ledger",
    "match_score": 0.97,
    "status": "approved",
    "explanation": "Amount matches within $0.02 tolerance. Date within 3-day window."
  }],
  "total": 1
}
```

---

## Exceptions

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/exceptions` | List all exceptions with severity and classification. |
| `POST` | `/api/exceptions` | Create an exception manually. |
| `GET` | `/api/exceptions/{id}` | Get exception details. |
| `POST` | `/api/exceptions/{id}/assign` | Assign exception to a reviewer. |
| `POST` | `/api/exceptions/{id}/resolve` | Resolve an exception with reason and resolution. |

```json
// GET /api/exceptions
{
  "items": [{
    "exception_id": "uuid", "category": "duplicate_payment", "severity": "high",
    "status": "escalated", "confidence": 0.90, "description": "Potential duplicate payment detected"
  }],
  "total": 1
}
```

---

## Review Queue

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/review-queue` | List pending HITL review items. |
| `POST` | `/api/review-queue` | Add an item to the review queue. |
| `GET` | `/api/review-queue/{id}` | Get review item details. |
| `POST` | `/api/review-queue/{id}/approve` | Approve a review item. |
| `POST` | `/api/review-queue/{id}/reject` | Reject a review item. |

---

## Evidence Binder

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/evidence-binder` | List evidence binders. |
| `POST` | `/api/evidence-binder` | Create a new evidence binder for a period. |
| `GET` | `/api/evidence-binder/{id}` | Get binder contents and seal status. |
| `POST` | `/api/evidence-binder/{id}/add-section` | Add a section (docs, recons, exceptions). |
| `POST` | `/api/evidence-binder/{id}/finalize` | Seal the binder with SHA-256 hash. |

```json
// POST /api/evidence-binder/{id}/finalize
{ "binder_id": "uuid", "status": "finalized", "seal_hash": "sha256:abcdef...", "finalized_at": "2026-03-13T18:00:00" }
```

---

## Race Control

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/race-control` | Live dashboard: phase, lanes, scoreboard, CFO cockpit, reasoning. |
| `GET` | `/api/race-control/scoreboard` | Scoreboard metrics only. |

```json
// GET /api/race-control (abbreviated)
{
  "phase": "QUALIFYING",
  "lanes": {
    "ingest": { "status": "green", "count": 5 },
    "reconcile": { "status": "green", "approved": 3 },
    "exceptions": { "status": "yellow", "open": 2 }
  },
  "scoreboard": { "match_rate": 94.5, "exceptions_open": 2 },
  "reasoning": "Race Control agent assessed 5 documents..."
}
```

---

## Voice Assistant

| Method | Path | Description |
|--------|------|-------------|
| `WS` | `/ws/voice` | WebSocket for real-time Gemini Live voice interaction. |
| `GET` | `/api/voice/sessions` | List active voice sessions. |
| `POST` | `/api/voice/sessions` | Create a new voice session. |

The WebSocket endpoint accepts audio frames and returns text/audio responses. Gemini Live handles speech recognition, tool calling (get_exceptions, approve_exception, etc.), and text-to-speech.

---

## Gradient AI

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/gradient/training/start` | Start a Gradient AI fine-tuning job. |
| `GET` | `/api/gradient/training/{id}` | Get training job status. |
| `POST` | `/api/gradient/inference` | Run inference against a trained model. |
| `GET` | `/api/gradient/provenance/{id}` | Get model provenance and lineage. |

---

## Audit Log

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/audit` | Return the most recent audit events. Accepts `?limit=N`. |

```json
// GET /api/audit?limit=2
{
  "events": [
    {
      "event_id": "uuid", "trace_id": "uuid", "ts": "2026-03-13T12:00:00",
      "action": "agent_auto_resolve", "entity_type": "exception", "entity_id": "uuid",
      "detail": { "confidence": 0.95, "reasoning": "Low-severity timing difference" }
    }
  ],
  "total": 42
}
```

---

## Agent Loop

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/agent/cycle` | Run one full perceive-decide-act cycle. |
| `GET` | `/api/agent/cycles` | List recent agent cycle history. |
| `GET` | `/api/agent/cycle/{id}` | Get specific cycle detail with full decision trace. |
| `GET` | `/api/agent/perceive` | Read-only perception of current system state. |
