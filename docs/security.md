# Security Guide

> LedgerLive is designed for finance operations where data integrity, access control, and auditability are non-negotiable.

---

## Authentication

LedgerLive uses a `SECRET_KEY` environment variable for JWT token signing.

**Current state**: JWT infrastructure is in place (Wave 12: Auth). In `DEMO` and `LOCAL` modes, authentication is relaxed to enable rapid testing and judging. In `PROD` mode, all mutating endpoints require a valid Bearer token.

**Planned enhancements**:

- SSO/SCIM integration (Wave 122) for enterprise identity providers.
- RBAC and ABAC policy engine (Waves 121-130) for fine-grained access control.
- Session management with refresh token rotation.

**Recommendation**: Always set a strong, unique `SECRET_KEY` in production. Never reuse the default value.

---

## CORS Configuration

The API applies CORS middleware via FastAPI:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production**: Replace `allow_origins=["*"]` with your specific frontend domain(s). This prevents cross-origin requests from unauthorized sites.

---

## Secrets Management

All secrets are read from environment variables. The `.env.example` file documents every variable without containing real values.

| Secret | Variable | Notes |
|--------|----------|-------|
| JWT signing key | `SECRET_KEY` | Must be 32+ random characters in production. |
| Gemini API key | `GEMINI_API_KEY` | Required only when `LLM_PROVIDER=GEMINI`. |
| Airia API key | `AIRIA_API_KEY` | Required for Airia platform integration. |
| DigitalOcean token | `DIGITALOCEAN_TOKEN` | Required for DO deployment. |
| Gradient AI key | `GRADIENT_AI_API_KEY` | Required for Gradient inference. |
| Database credentials | `DATABASE_URL` | Use a connection string with credentials for PostgreSQL. |

**Rules**:

- Never commit `.env` files to version control (`.gitignore` excludes them).
- Use your platform's secret manager (GCP Secret Manager, DO App Platform secrets) in production.
- Rotate any secret that may have been exposed.

---

## Audit Trail and Tamper Evidence

Every state mutation in LedgerLive emits an audit event through the `emit_audit_event()` function:

```json
{
  "event_id": "uuid",
  "trace_id": "uuid",
  "ts": "2026-03-13T12:00:00",
  "action": "agent_auto_resolve",
  "entity_type": "exception",
  "entity_id": "uuid",
  "detail": { "confidence": 0.95, "reasoning": "..." }
}
```

The audit log is append-only. Events are never modified or deleted during a session.

**SHA-256 sealing**: Evidence binders are finalized with a SHA-256 hash of all contents. Any post-finalization modification invalidates the seal. Checkpoint hashes appear throughout the system (race control, agent cycles, binder seals) to enable tamper detection.

---

## Input Validation

LedgerLive validates all inputs using Pydantic models and FastAPI's built-in request validation:

- Request bodies are parsed against typed schemas before reaching service logic.
- Path parameters and query parameters are type-checked automatically.
- Unknown fields are rejected (strict mode where applicable).
- Numeric ranges, string lengths, and enum constraints are enforced at the schema level.

---

## Fail-Closed Design

When the agent cannot confidently classify or resolve an exception, it escalates rather than guessing. This fail-closed principle means:

- Exceptions above the materiality threshold always require human approval.
- Agent confidence scores below 70% trigger escalation instead of auto-resolution.
- Workflow stages do not advance while blocking exceptions remain open.
- The evidence binder cannot be finalized until all items are resolved.
