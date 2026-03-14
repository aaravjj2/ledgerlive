# Deployment Guide

> LedgerLive supports local development, Docker, Google Cloud Run, and DigitalOcean App Platform.

---

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm 9+
- (Optional) Docker and Docker Compose
- (Optional) `gcloud` CLI for Cloud Run
- (Optional) `doctl` CLI for DigitalOcean

---

## Option 1: Local Development

The fastest path to a running instance.

```bash
# Clone the repository
git clone https://github.com/aaravjj2/ledgerlive.git
cd ledgerlive

# Copy environment template
cp .env.example .env

# Install Python dependencies
cd apps/api
pip install -r requirements.txt
# or: pip install -e .
cd ../..

# Install web dependencies
cd apps/web
npm install
cd ../..

# Start in demo mode (API on :8090, Web on :4173)
make demo
```

Open `http://127.0.0.1:4173` for the frontend and `http://127.0.0.1:8090/healthz` for the API.

### Development Mode (Hot Reload)

```bash
make dev
```

This starts the API with `--reload` on port 8090 and the Vite dev server on port 5173.

---

## Option 2: Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

The `docker-compose.yml` exposes:

| Service | Port | Description |
|---------|------|-------------|
| `api` | 8090 | FastAPI backend |
| `web` | 4173 | Vite production preview |

### Docker Build Only

```bash
# API image
docker build -t ledgerlive-api -f apps/api/Dockerfile .

# Web image
docker build -t ledgerlive-web -f apps/web/Dockerfile .
```

---

## Option 3: Google Cloud Run

Cloud Run runs the API as a single containerized service.

### Step 1: Build and Push

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build with Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ledgerlive-api

# Or build locally and push
docker build -t gcr.io/YOUR_PROJECT_ID/ledgerlive-api -f apps/api/Dockerfile .
docker push gcr.io/YOUR_PROJECT_ID/ledgerlive-api
```

### Step 2: Deploy

```bash
gcloud run deploy ledgerlive-api \
  --image gcr.io/YOUR_PROJECT_ID/ledgerlive-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars APP_MODE=PROD,LLM_PROVIDER=GEMINI,E2E_MODE=0 \
  --set-env-vars SECRET_KEY=your-production-secret \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10
```

Cloud Run automatically sets the `$PORT` environment variable. The `Procfile` references it:

```
web: cd apps/api && uvicorn app.main:app --host=0.0.0.0 --port=$PORT --workers=2
```

---

## Option 4: DigitalOcean App Platform

### Using the App Spec

Create an `app.yaml` for DigitalOcean App Platform:

```yaml
name: ledgerlive
services:
  - name: api
    github:
      repo: aaravjj2/ledgerlive
      branch: main
      deploy_on_push: true
    source_dir: /
    build_command: cd apps/api && pip install -r requirements.txt
    run_command: cd apps/api && uvicorn app.main:app --host=0.0.0.0 --port=8080 --workers=2
    environment_slug: python
    instance_size_slug: basic-xxs
    instance_count: 1
    envs:
      - key: APP_MODE
        value: PROD
      - key: LLM_PROVIDER
        value: DEMO
      - key: SECRET_KEY
        type: SECRET
        value: your-production-secret
```

### Deploy via CLI

```bash
doctl apps create --spec app.yaml
```

### Deploy via Dashboard

1. Go to https://cloud.digitalocean.com/apps
2. Connect your GitHub repository.
3. Set the build and run commands as shown above.
4. Add environment variables in the Settings tab.

---

## Environment Variables Reference

See [configuration.md](./configuration.md) for the complete environment variables reference.

The minimum required variables for production:

| Variable | Required | Example |
|----------|----------|---------|
| `APP_MODE` | Yes | `PROD` |
| `SECRET_KEY` | Yes | A random 32+ character string |
| `LLM_PROVIDER` | Yes | `GEMINI`, `OLLAMA`, or `DEMO` |
| `DATABASE_URL` | Recommended | `postgresql+asyncpg://...` |

---

## Verifying a Deployment

After deploying, confirm the service is healthy:

```bash
# Health check
curl https://your-deployment-url/healthz

# Run a quick smoke test
curl https://your-deployment-url/api/race-control
curl https://your-deployment-url/api/documents
curl https://your-deployment-url/api/audit?limit=5
```

You should see `"status": "ok"` in the health response and populated data in the other endpoints when running in DEMO mode.

---

## Running Tests

```bash
# Unit and integration tests
make test

# E2E tests (requires running API + Web)
make e2e-mcp

# Full gate checks
make gates
```
