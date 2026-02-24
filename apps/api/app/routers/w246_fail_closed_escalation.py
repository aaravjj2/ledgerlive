"""Wave 246: Fail-Closed Escalation v1 Router â€” Uncertain steps become approval-required. If risk rules fail, creates incident and pauses automation. Deterministic escalation logic.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w246_fail_closed_escalation import service

router = APIRouter(tags=["Fail-Closed Escalation v1"])

@router.get("/api/fail-closed-escalation")
async def api_fail_closed_escalation_w246_list_escalations(limit: int = 100):
    """List fail-closed escalations"""
    items = service.list_escalations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/fail-closed-escalation", status_code=201)
async def api_fail_closed_escalation_w246_create_escalation(request: Request):
    """Create fail-closed escalation"""
    data = await request.json()
    item = service.create_escalation(data)
    return item

@router.get("/api/fail-closed-escalation/report")
async def api_fail_closed_escalation_w246_escalation_report(limit: int = 100):
    """Get escalation report"""
    items = service.escalation_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/fail-closed-escalation/{escalation_id}")
async def api_fail_closed_escalation_w246_get_escalation(escalation_id: str):
    """Get escalation details"""
    item = service.get_escalation(escalation_id)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed_escalation not found")
    return item

@router.post("/api/fail-closed-escalation/{escalation_id}/approve")
async def api_fail_closed_escalation_w246_approve_escalation(escalation_id: str, request: Request):
    """Approve escalated step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_escalation(escalation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed_escalation not found")
    return item

@router.post("/api/fail-closed-escalation/{escalation_id}/create-incident")
async def api_fail_closed_escalation_w246_create_incident(escalation_id: str, request: Request):
    """Create incident from escalation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.create_incident(escalation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed_escalation not found")
    return item

@router.post("/api/fail-closed-escalation/{escalation_id}/resume")
async def api_fail_closed_escalation_w246_resume_automation(escalation_id: str, request: Request):
    """Resume paused automation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resume_automation(escalation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed_escalation not found")
    return item

