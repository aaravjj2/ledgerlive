"""Wave 327: Redaction Events v1 Router — Redaction actions become first-class security events with evidence links.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w327_redaction_events_v1 import service

router = APIRouter(tags=["Redaction Events v1"])

@router.get("/api/redaction-events-v1")
async def api_redaction_events_v1_w327_list_redactions(limit: int = 100):
    """List redaction events"""
    items = service.list_redactions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/redaction-events-v1", status_code=201)
async def api_redaction_events_v1_w327_create_redaction(request: Request):
    """Create redaction event"""
    data = await request.json()
    item = service.create_redaction(data)
    return item

@router.get("/api/redaction-events-v1/report")
async def api_redaction_events_v1_w327_redaction_report(limit: int = 100):
    """Get redaction events report"""
    items = service.redaction_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/redaction-events-v1/{redaction_id}")
async def api_redaction_events_v1_w327_get_redaction(redaction_id: str):
    """Get redaction details"""
    item = service.get_redaction(redaction_id)
    if not item:
        raise HTTPException(status_code=404, detail="redaction_events_v1 not found")
    return item

@router.post("/api/redaction-events-v1/{redaction_id}/evidence")
async def api_redaction_events_v1_w327_link_evidence(redaction_id: str, request: Request):
    """Link evidence to redaction"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_evidence(redaction_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="redaction_events_v1 not found")
    return item

@router.post("/api/redaction-events-v1/{redaction_id}/reverse")
async def api_redaction_events_v1_w327_reverse_redaction(redaction_id: str, request: Request):
    """Reverse redaction if allowed"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reverse_redaction(redaction_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="redaction_events_v1 not found")
    return item
