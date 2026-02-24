"""Golden Scenario Router — DEMO+E2E-only endpoints for Race Control golden state.

PROJECT_ID: LEDGERLIVE
GUARD: All endpoints return HTTP 403 unless APP_MODE=DEMO and E2E_MODE=1.

Endpoints:
  POST /api/ops/golden-scenario-run      → seed + return IDs
  POST /api/ops/golden-scenario-reset    → clear golden state
  GET  /api/ops/e2e-assertions           → computed truthful assertions
  GET  /api/ops/e2e_assertions           (alias with underscore)
  POST /api/ops/rc-approval/{id}/approve → approve a pending step
  POST /api/ops/rc-approval/{id}/reject  → reject
  POST /api/ops/export/telemetry-pack    → generate telemetry, return PASS + sha256
  POST /api/ops/export/court-pack        → generate court pack, return PASS + sha256
  POST /api/ops/replay/regenerate-binder → regen binder, return hash
  GET  /api/ops/security-event/{id}      → get security event
  GET  /api/ops/security-events          → list security events
  POST /api/ops/security-event/{id}/fix-path → trigger fix path
  POST /api/ops/channel/send-approval    → mock channel approval send
  POST /api/ops/atlassian/create-jira    → mock Jira issue creation
  POST /api/ops/atlassian/create-confluence → mock Confluence page
  GET  /api/ops/checkpoint/{cp_id}/why   → dossier for checkpoint
  GET  /api/ops/checkpoint/{cp_id}/verify → verify checkpoint
  GET  /api/ops/incident/{inc_id}/why    → dossier for incident
  GET  /api/ops/approval/{ap_id}/why     → dossier for approval
  POST /api/ops/update-baseline          → write current binder hash as baseline
  POST /api/ops/tamper-artifact          → controlled tamper hook (negative tests)
"""
import os

from fastapi import APIRouter, Depends, HTTPException, Request

from app.services.golden_scenario import service


def require_e2e_mode() -> None:
    """FastAPI dependency: block access unless APP_MODE=DEMO and E2E_MODE=1.

    Checks os.getenv at request time so it is patchable in tests.
    """
    app_mode = os.getenv("APP_MODE", "LOCAL")
    e2e_mode = os.getenv("E2E_MODE", "0") == "1"
    if not (app_mode == "DEMO" and e2e_mode):
        raise HTTPException(
            status_code=403,
            detail=(
                "Golden Scenario endpoints require APP_MODE=DEMO and E2E_MODE=1. "
                f"Got APP_MODE={app_mode!r}, E2E_MODE={os.getenv('E2E_MODE', '0')!r}."
            ),
        )


router = APIRouter(
    tags=["Golden Scenario / E2E Ops"],
    dependencies=[Depends(require_e2e_mode)],
)


# ── Seed / Reset ─────────────────────────────────────────────────────

@router.post("/api/ops/golden-scenario-run", status_code=201)
async def golden_scenario_run():
    """Seed the golden Race Control scenario into all in-memory stores."""
    return service.seed()


@router.post("/api/ops/golden-scenario-reset", status_code=200)
async def golden_scenario_reset():
    """Clear golden scenario fixtures from all in-memory stores."""
    return service.reset()


# ── E2E Assertions ────────────────────────────────────────────────────

@router.get("/api/ops/e2e-assertions")
async def e2e_assertions():
    """Return deterministic expected IDs, counts, and hashes for golden scenario assertions."""
    return service.get_assertions()


@router.get("/api/ops/e2e_assertions")
async def e2e_assertions_underscore():
    """Alias with underscore."""
    return service.get_assertions()


# ── Approval Actions ─────────────────────────────────────────────────

@router.post("/api/ops/rc-approval/{approval_id}/approve", status_code=200)
async def approve_step(approval_id: str):
    """Approve a pending approval step."""
    item = service.approve_step(approval_id)
    if not item:
        raise HTTPException(status_code=404, detail="Approval not found")
    return item


@router.post("/api/ops/rc-approval/{approval_id}/reject", status_code=200)
async def reject_step(approval_id: str, request: Request):
    """Reject an approval step."""
    try:
        data = await request.json()
    except Exception:
        data = {}
    from app.services.w239_rc_approval import service as appr_svc
    from app.main import emit_audit_event
    item = appr_svc._store.get(approval_id)
    if not item:
        raise HTTPException(status_code=404, detail="Approval not found")
    item["status"] = "rejected"
    emit_audit_event("grc_reject_step", "rc_approval", approval_id, {"data": data})
    return item


# ── Exports ──────────────────────────────────────────────────────────

@router.post("/api/ops/export/telemetry-pack", status_code=201)
async def export_telemetry_pack():
    """Generate telemetry pack for golden scenario and return PASS badge."""
    return service.generate_telemetry_pack()


@router.post("/api/ops/export/court-pack", status_code=201)
async def export_court_pack():
    """Generate court pack for golden scenario and return PASS badge."""
    return service.generate_court_pack()


@router.post("/api/ops/replay/regenerate-binder", status_code=201)
async def regenerate_binder():
    """Regenerate replay binder and return stable hash."""
    return service.regenerate_binder()


# ── Security Events ───────────────────────────────────────────────────

@router.get("/api/ops/security-events")
async def list_security_events():
    """List all security events in golden scenario."""
    items = service.list_security_events()
    return {"items": items, "total": len(items)}


@router.get("/api/ops/security-event/{event_id}")
async def get_security_event(event_id: str):
    """Get a single security event."""
    evt = service.get_security_event(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Security event not found")
    return evt


@router.post("/api/ops/security-event/{event_id}/fix-path", status_code=200)
async def security_fix_path(event_id: str):
    """Trigger the approved fix path → resolves the blocked security event."""
    evt = service.security_fix_path(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Security event not found")
    return evt


# ── Channel Actions ───────────────────────────────────────────────────

@router.post("/api/ops/channel/send-approval", status_code=201)
async def channel_send_approval(request: Request):
    """Send approval request to mock channel (email/chat)."""
    data = await request.json()
    approval_id = data.get("approval_id", "")
    channel = data.get("channel", "email")
    return service.send_channel_approval(approval_id, channel)


# ── Atlassian Mocks ───────────────────────────────────────────────────

@router.post("/api/ops/atlassian/create-jira", status_code=201)
async def atlassian_create_jira(request: Request):
    """Create a mock Jira issue for an overdue approval."""
    data = await request.json()
    approval_id = data.get("approval_id", "")
    return service.create_jira_issue(approval_id)


@router.post("/api/ops/atlassian/create-confluence", status_code=201)
async def atlassian_create_confluence():
    """Create a mock Confluence Race Weekend Close Report page."""
    return service.create_confluence_page()


# ── Dossier / Why / Verify ────────────────────────────────────────────

@router.get("/api/ops/checkpoint/{cp_id}/why")
async def checkpoint_why(cp_id: str):
    """Return dossier / evidence for a checkpoint."""
    from app.services.w228_close_checkpoint import service as cp_svc
    item = cp_svc._store.get(cp_id)
    if not item:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    return {
        "checkpoint_id": cp_id,
        "dossier_type": "checkpoint_why",
        "checkpoint": item,
        "evidence": [
            {"type": "gate_run", "result": item.get("gate_result"), "criteria_met": item.get("criteria_met")},
            {"type": "audit_trail", "ref": f"grc-audit-{cp_id[:8]}"},
        ],
        "narrative": f"Checkpoint '{item.get('checkpoint_name')}' gate ran with result {item.get('gate_result')}.",
    }


@router.get("/api/ops/checkpoint/{cp_id}/verify")
async def checkpoint_verify(cp_id: str):
    """Verify a checkpoint deterministically."""
    from app.services.w228_close_checkpoint import service as cp_svc
    item = cp_svc._store.get(cp_id)
    if not item:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    return {
        "checkpoint_id": cp_id,
        "verify_result": "PASS" if item.get("criteria_met") else "FAIL",
        "criteria_met": item.get("criteria_met"),
        "gate_result": item.get("gate_result"),
    }


@router.get("/api/ops/incident/{inc_id}/why")
async def incident_why(inc_id: str):
    """Return dossier / evidence for an incident."""
    from app.services.w233_incident_log import service as inc_svc
    item = inc_svc._store.get(inc_id)
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {
        "incident_id": inc_id,
        "dossier_type": "incident_why",
        "incident": item,
        "evidence": [
            {"type": "sla_record", "breach": True, "sla_threshold_h": 48},
            {"type": "audit_trail", "ref": f"grc-audit-{inc_id[:8]}"},
        ],
        "narrative": f"Incident '{item.get('incident_title')}' reported at {item.get('reported_at')}.",
    }


@router.get("/api/ops/approval/{ap_id}/why")
async def approval_why(ap_id: str):
    """Return dossier / evidence for an approval step."""
    from app.services.w239_rc_approval import service as appr_svc
    item = appr_svc._store.get(ap_id)
    if not item:
        raise HTTPException(status_code=404, detail="Approval not found")
    return {
        "approval_id": ap_id,
        "dossier_type": "approval_why",
        "approval": item,
        "evidence": [
            {"type": "approver_list", "approvers": item.get("approvers", [])},
            {"type": "audit_trail", "ref": f"grc-audit-{ap_id[:8]}"},
        ],
        "narrative": f"Approval step {item.get('approval_level')}/{item.get('total_levels')} status: {item.get('status')}.",
    }


# ── Baseline Management ───────────────────────────────────────────────

@router.post("/api/ops/update-baseline", status_code=200)
async def update_baseline():
    """Write the current binder hash to the baseline file.

    Call once after a clean seed to record the expected hash.
    Subsequent test runs will compare against this value.
    """
    h = service.write_baseline_binder_hash()
    return {"baseline_written": True, "binder_hash": h}


# ── Tamper Hook (controlled negative test support) ────────────────────

@router.post("/api/ops/tamper-artifact", status_code=200)
async def tamper_artifact(request: Request):
    """Force-set a field in an artifact to simulate tampering.

    Payload: {"artifact_key": "telemetry_pack", "field": "status", "value": "TAMPERED"}

    After tampering, get_assertions() will return a different assertions_signature,
    proving the signature is sensitive to artifact state changes.
    """
    data = await request.json()
    artifact_key = data.get("artifact_key", "")
    field = data.get("field", "")
    value = data.get("value")
    try:
        result = service.tamper_artifact(artifact_key, field, value)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"tampered": True, "artifact": result}
