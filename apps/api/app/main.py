"""LedgerLive — Finance Ops Close Agent API

This is the main FastAPI application entry point.
PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import uuid
import datetime as dt
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_MODE, PROJECT_ID, LLM_PROVIDER


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup / shutdown."""
    print(f"[LedgerLive] Starting in {APP_MODE} mode | LLM={LLM_PROVIDER}")
    yield
    print("[LedgerLive] Shutting down")


app = FastAPI(
    title="LedgerLive API",
    description="Finance Ops Close Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────
@app.get("/healthz")
async def healthz():
    return {
        "project": PROJECT_ID,
        "status": "ok",
        "mode": APP_MODE,
        "llm": LLM_PROVIDER,
        "ts": dt.datetime.utcnow().isoformat(),
    }


# ── Audit event spine ────────────────────────────────────────────────
AUDIT_LOG: list[dict] = []


def emit_audit_event(
    action: str,
    entity_type: str,
    entity_id: str,
    detail: dict | None = None,
    trace_id: str | None = None,
) -> dict:
    """Append-only audit event emitter. Every state mutation MUST call this."""
    event = {
        "event_id": str(uuid.uuid4()),
        "trace_id": trace_id or str(uuid.uuid4()),
        "ts": dt.datetime.utcnow().isoformat(),
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "detail": detail or {},
    }
    AUDIT_LOG.append(event)
    return event


@app.get("/api/audit")
async def get_audit_log(limit: int = 100):
    """Return the most recent audit events."""
    return {"events": AUDIT_LOG[-limit:], "total": len(AUDIT_LOG)}


# ── Wave routers will be registered below this line ──────────────────
