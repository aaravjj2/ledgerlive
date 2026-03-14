"""Airia Webhook Router — Inbound webhook endpoint for Airia platform integration.

Airia can call these endpoints to trigger agent actions:
  POST /api/webhook/airia           → receive Airia webhook and trigger agent cycle
  GET  /api/webhook/airia/log       → recent webhook event log
  GET  /api/webhook/airia/stats     → delivery statistics
  POST /api/webhook/airia/export    → export agent results to Airia-compatible format

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import datetime as dt
import hashlib
import uuid

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.main import emit_audit_event

router = APIRouter(tags=["Airia Webhook"])


class AiriaWebhookPayload(BaseModel):
    """Payload structure Airia sends when triggering the agent."""
    event_type: str = "trigger_cycle"
    data: dict = {}
    callback_url: str = ""


class AiriaExportRequest(BaseModel):
    """Request to export agent results for Airia."""
    format: str = "airia_v1"
    include_traces: bool = True


# In-memory webhook event log
_inbound_log: list[dict] = []


@router.post("/api/webhook/airia", status_code=200)
async def receive_airia_webhook(payload: AiriaWebhookPayload, request: Request):
    """Receive inbound webhook from Airia platform and trigger agent cycle.

    Airia calls this endpoint to:
    - Trigger a perceive→decide→act cycle
    - Request an export of agent results
    - Query agent status

    Returns the cycle result if event_type is 'trigger_cycle'.
    """
    from app.services.agent_loop import run_cycle, perceive
    from app.services.airia_webhook import post_to_airia

    event_id = str(uuid.uuid4())
    entry = {
        "event_id": event_id,
        "ts": dt.datetime.utcnow().isoformat(),
        "event_type": payload.event_type,
        "data": payload.data,
        "callback_url": payload.callback_url,
        "source_ip": request.client.host if request.client else "unknown",
    }

    result: dict = {}

    if payload.event_type == "trigger_cycle":
        # Run full perceive→decide→act cycle
        cycle = run_cycle()
        result = {
            "status": "cycle_complete",
            "cycle_id": cycle["cycle_id"],
            "summary": cycle["summary"],
            "actions_executed": cycle["phases"]["act"]["total_actions"],
            "successes": cycle["phases"]["act"]["successes"],
        }
        entry["cycle_id"] = cycle["cycle_id"]

    elif payload.event_type == "query_state":
        # Just perceive, don't act
        perception = perceive()
        result = {
            "status": "state_returned",
            "perception": perception,
        }

    elif payload.event_type == "ping":
        result = {"status": "pong", "project": "LEDGERLIVE"}

    else:
        result = {"status": "unknown_event_type", "event_type": payload.event_type}

    entry["result"] = result
    _inbound_log.append(entry)

    # Emit audit event
    emit_audit_event("webhook_received", "airia_webhook", event_id, {
        "event_type": payload.event_type,
        "has_callback": bool(payload.callback_url),
    })

    # If callback URL provided, post result back
    if payload.callback_url:
        post_to_airia("cycle_result", result)

    return {
        "event_id": event_id,
        **result,
    }


@router.get("/api/webhook/airia/log")
async def get_webhook_log(limit: int = 50):
    """Return recent inbound webhook events."""
    from app.services.airia_webhook import get_webhook_log as get_outbound_log
    return {
        "inbound": _inbound_log[-limit:],
        "outbound": get_outbound_log(limit),
        "total_inbound": len(_inbound_log),
    }


@router.get("/api/webhook/airia/stats")
async def get_webhook_stats():
    """Return webhook delivery statistics."""
    from app.services.airia_webhook import get_webhook_stats
    outbound = get_webhook_stats()
    return {
        "inbound_total": len(_inbound_log),
        "inbound_by_type": _count_by_type(),
        "outbound": outbound,
        "integration_status": "active" if len(_inbound_log) > 0 or outbound["total_events"] > 0 else "idle",
    }


@router.post("/api/webhook/airia/export")
async def export_for_airia(req: AiriaExportRequest):
    """Export agent results in Airia-compatible format.

    Produces a structured bundle Airia can ingest:
    - Agent cycle summaries
    - Decision traces with reasoning
    - Webhook delivery log
    - Evidence checksums
    """
    from app.services.agent_loop import get_cycle_log
    from app.services.airia_webhook import get_webhook_log, get_webhook_stats
    from app.services.cfo_scenario import get_cfo_metrics

    cycles = get_cycle_log(50)
    metrics = get_cfo_metrics()
    webhook_log = get_webhook_log(50)
    stats = get_webhook_stats()

    bundle = {
        "format": req.format,
        "project": "LEDGERLIVE",
        "exported_at": dt.datetime.utcnow().isoformat(),
        "agent_cycles": [
            {
                "cycle_id": c["cycle_id"],
                "ts": c["ts"],
                "elapsed_ms": c["elapsed_ms"],
                "summary": c["summary"],
                "actions": c["phases"]["decide"]["actions_planned"],
                "successes": c["phases"]["act"]["successes"],
            }
            for c in cycles
        ] if req.include_traces else [],
        "cfo_metrics": metrics,
        "webhook_stats": stats,
        "checksum": hashlib.sha256(
            f"export-{len(cycles)}-{stats['total_events']}".encode()
        ).hexdigest()[:16],
    }

    emit_audit_event("airia_export", "webhook", "export", {
        "format": req.format,
        "cycles_exported": len(cycles),
    })

    return bundle


def _count_by_type() -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in _inbound_log:
        et = entry.get("event_type", "unknown")
        counts[et] = counts.get(et, 0) + 1
    return counts
