# Frequently Asked Questions

---

### 1. What is LedgerLive?

LedgerLive is an AI-powered finance operations platform that automates the month-end close process. It ingests financial documents, runs OCR and field extraction, performs multi-way reconciliation, triages exceptions with AI-assigned severity, routes items for human review, and assembles tamper-evident evidence binders -- all with a full audit trail.

---

### 2. How does the reconciliation work?

The reconciliation engine scores candidate transaction pairs across three dimensions: amount match (with configurable tolerance), date proximity (within a business-day window), and reference number similarity (fuzzy string matching). The composite score determines whether a pair is auto-approved (>= 0.85), flagged for review (0.60-0.85), or classified as an exception (< 0.60). Every result includes a human-readable explanation.

See [how-it-works.md](./how-it-works.md) for the full algorithm.

---

### 3. Is it production-ready?

LedgerLive is built for hackathon demonstration and early-stage validation. The core close flow (ingest, OCR, reconciliation, exceptions, review, evidence binder) is fully functional with 340+ service waves and 4,000+ passing tests. For production use, you would want to:

- Replace the in-memory stores with a persistent database (PostgreSQL is supported).
- Enable JWT authentication and restrict CORS origins.
- Configure a production LLM provider (Gemini, OpenAI) instead of the DEMO mock.
- Deploy on Cloud Run or DigitalOcean with proper secret management.

---

### 4. What AI models does it use?

LedgerLive supports multiple LLM providers via the `LLM_PROVIDER` environment variable:

- **DEMO**: Deterministic mock responses. No external API calls. Works offline.
- **OLLAMA**: Local model inference via Ollama (default model: `devstral`).
- **OPENAI**: OpenAI API (GPT-4, GPT-3.5).
- **GEMINI**: Google Gemini API, including Gemini Live for voice interactions.

The agent's core triage logic is rule-based and deterministic. LLM calls enhance explanations and natural-language reasoning but are not required for the close flow to function.

---

### 5. Can I use my own LLM?

Yes. Set `LLM_PROVIDER=OLLAMA` and `OLLAMA_MODEL=your-model-name` to point at any model served by a local Ollama instance. For cloud-hosted models, you can add a new adapter following the pattern in `app/services/w177_gemini_adapter.py` or `app/services/w179_gradient_adapter.py`.

---

### 6. How are exceptions classified?

The exception classifier assigns each mismatch a **category** and **severity**:

**Categories**: `timing_difference`, `rounding_variance`, `duplicate_payment`, `missing_entry`, `amount_mismatch`, `unidentified`.

**Severities**:
- **Low/Info**: Below materiality threshold. Auto-resolved at 95% confidence.
- **Medium**: Moderate issues. Auto-resolved at 75% confidence if pattern-matched.
- **High**: Large variances, duplicates, or unidentifiable items. Always escalated to the review queue.

---

### 7. What is the F1 metaphor about?

LedgerLive uses a Formula 1 racing metaphor to make the close process intuitive:

- **Pit Stop** = Document ingestion (prep work)
- **Qualifying** = Reconciliation (proving accuracy)
- **Safety Car** = Exceptions (process pauses for issues)
- **Race** = Human review (active resolution)
- **Podium** = Evidence binder finalized (close complete)

The Race Control dashboard (`/api/race-control`) displays real-time lane statuses, a scoreboard, and phase indicators using this metaphor.

---

### 8. How do I add a new data source?

LedgerLive has a connector framework (Waves 15, 41-44) with existing adapters for QuickBooks Online (QBO), Xero, and Plaid. To add a new data source:

1. Create a new router in `app/routers/` following the pattern of `w42_qbo_connector.py`.
2. Create a matching service in `app/services/` for the business logic.
3. Register the router in `app/main.py`.
4. Add tests in `tests/`.
5. Map the source fields to the reconciliation engine's expected format using the Mapping Studio (Wave 45).

---

### 9. What compliance standards does it support?

LedgerLive includes compliance-oriented features for:

- **SOX**: Segregation of duties, evidence binders, audit trails (Waves 101, 37, 09).
- **ISO 27001**: Information security mapping (Wave 102).
- **SOC 2**: Evidence collection and export (Wave 101).
- **GDPR**: Data redaction and privacy controls (Waves 104, 25).
- **eDiscovery**: Legal hold and document export (Wave 103).

The compliance bundle (`/api/compliance-bundle`) packages all evidence for audit submission.

---

### 10. How do I run it in production?

See the [Deployment Guide](./deployment.md) for step-by-step instructions. The short version:

1. Set `APP_MODE=PROD`, a strong `SECRET_KEY`, and your preferred `LLM_PROVIDER`.
2. Configure a PostgreSQL `DATABASE_URL`.
3. Deploy to Google Cloud Run or DigitalOcean App Platform.
4. Verify with `curl https://your-url/healthz`.

The Procfile-based deployment works with any platform that supports it (Heroku, Railway, Render).
