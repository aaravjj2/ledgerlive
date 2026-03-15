# ── LedgerLive API ── Python 3.12 FastAPI backend ──────────────────
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ── Dependencies ───────────────────────────────────────────────────
# Copy requirements from repo root (build context is repo root via
# docker-compose context/dockerfile directives).
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Application code ──────────────────────────────────────────────
COPY apps/api/app /app/app

# ── Runtime config ────────────────────────────────────────────────
ENV APP_MODE=DEMO \
    E2E_MODE=1

EXPOSE 8090

# ── Healthcheck ───────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8090/healthz')" || exit 1

# ── Entrypoint ────────────────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090"]
