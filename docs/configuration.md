# Configuration Reference

> All configuration is driven by environment variables.
> Copy `.env.example` to `.env` and adjust values for your environment.

---

## Core Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_MODE` | string | `LOCAL` | Application mode. Controls demo data seeding and feature flags. |
| `LLM_PROVIDER` | string | `DEMO` | Which LLM backend to use for AI decisions. |
| `SECRET_KEY` | string | `dev-secret-key-change-in-prod` | Secret key for JWT signing. **Change in production.** |
| `E2E_MODE` | string | `0` | Set to `1` to enable E2E and golden scenario endpoints. |

### APP_MODE Options

| Value | Behavior |
|-------|----------|
| `LOCAL` | Seeds demo data on startup. Intended for development. |
| `DEMO` | Seeds demo data on startup. Intended for demos and hackathon judging. |
| `PROD` | No demo data seeded. Requires real data sources and authentication. |

### LLM_PROVIDER Options

| Value | Backend | Requirements |
|-------|---------|--------------|
| `DEMO` | Deterministic mock responses | None. Works offline. |
| `OLLAMA` | Local Ollama instance | Ollama running locally with the configured model. |
| `OPENAI` | OpenAI API | `OPENAI_API_KEY` environment variable. |
| `GEMINI` | Google Gemini API | `GEMINI_API_KEY` environment variable. |

---

## Database

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | `sqlite+aiosqlite:///./ledgerlive.db` | SQLAlchemy-compatible connection string. |

Supported databases:

- **SQLite** (default): `sqlite+aiosqlite:///./ledgerlive.db`
- **PostgreSQL**: `postgresql+asyncpg://user:pass@host:5432/dbname`

---

## Ports

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `API_PORT` | int | `8090` | FastAPI backend port. |
| `WEB_PORT` | int | `4173` | Vite production preview port. |
| `WEB_DEV_PORT` | int | `5173` | Vite development server port. |
| `PORT` | int | (unset) | Set automatically by Cloud Run / Heroku / DigitalOcean. Overrides `API_PORT`. |

---

## Google Cloud / Gemini

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GOOGLE_CLOUD_PROJECT` | string | (unset) | GCP project ID for Cloud Run and Gemini. |
| `GEMINI_API_KEY` | string | (unset) | Gemini API key for LLM and voice features. |
| `GEMINI_MODEL` | string | `gemini-2.0-flash-live` | Model name for voice interactions. |
| `GOOGLE_APPLICATION_CREDENTIALS` | string | (unset) | Path to GCP service account JSON. |

---

## DigitalOcean

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DIGITALOCEAN_TOKEN` | string | (unset) | DigitalOcean API token for deployment. |
| `GRADIENT_AI_API_KEY` | string | (unset) | Gradient AI inference key. |
| `SPACES_ACCESS_KEY` | string | (unset) | DigitalOcean Spaces access key (S3-compatible). |
| `SPACES_SECRET_KEY` | string | (unset) | DigitalOcean Spaces secret key. |

---

## Airia Platform

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AIRIA_API_KEY` | string | (unset) | Airia platform API key for agent orchestration. |
| `AIRIA_WEBHOOK_URL` | string | (unset) | Webhook URL for posting agent cycle results. |

---

## Ollama (Local LLM)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OLLAMA_MODEL` | string | `devstral` | Model name for local Ollama inference. |

---

## Optional Services

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `REDIS_URL` | string | (unset) | Redis connection URL for caching. |
| `GITLAB_TOKEN` | string | (unset) | GitLab personal access token for CI integration. |
