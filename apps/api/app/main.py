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
from app.routers.w01_close_period import router as w01_router
from app.routers.w02_entity import router as w02_router
from app.routers.w03_document_store import router as w03_router
from app.routers.w04_ocr_pipeline import router as w04_router
from app.routers.w05_extraction import router as w05_router
from app.routers.w06_reconciliation import router as w06_router
from app.routers.w07_exception import router as w07_router
from app.routers.w08_review_queue import router as w08_router
from app.routers.w09_evidence_binder import router as w09_router
from app.routers.w10_eval_harness import router as w10_router
from app.routers.w11_tenant import router as w11_router
from app.routers.w12_auth import router as w12_router
from app.routers.w13_workflow import router as w13_router
from app.routers.w14_notification import router as w14_router
from app.routers.w15_connector import router as w15_router
from app.routers.w16_vendor_master import router as w16_router
from app.routers.w17_chart_of_accounts import router as w17_router
from app.routers.w18_continuous_close import router as w18_router
from app.routers.w19_audit_integrity import router as w19_router
from app.routers.w20_signed_export import router as w20_router
from app.routers.w21_report import router as w21_router
from app.routers.w22_search_index import router as w22_router
from app.routers.w23_compliance_bundle import router as w23_router
from app.routers.w24_retention import router as w24_router
from app.routers.w25_data_privacy import router as w25_router
from app.routers.w26_performance import router as w26_router
from app.routers.w27_release_bundle import router as w27_router
from app.routers.w28_judge_demo import router as w28_router
from app.routers.w29_deploy_config import router as w29_router
from app.routers.w30_hardening import router as w30_router

app.include_router(w01_router)
app.include_router(w02_router)
app.include_router(w03_router)
app.include_router(w04_router)
app.include_router(w05_router)
app.include_router(w06_router)
app.include_router(w07_router)
app.include_router(w08_router)
app.include_router(w09_router)
app.include_router(w10_router)
app.include_router(w11_router)
app.include_router(w12_router)
app.include_router(w13_router)
app.include_router(w14_router)
app.include_router(w15_router)
app.include_router(w16_router)
app.include_router(w17_router)
app.include_router(w18_router)
app.include_router(w19_router)
app.include_router(w20_router)
app.include_router(w21_router)
app.include_router(w22_router)
app.include_router(w23_router)
app.include_router(w24_router)
app.include_router(w25_router)
app.include_router(w26_router)
app.include_router(w27_router)
app.include_router(w28_router)
app.include_router(w29_router)
app.include_router(w30_router)
