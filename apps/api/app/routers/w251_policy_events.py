"""Wave 251: Policy Events v1 Router — Policy denies, scope violations, and injection flags become structured security events with classification, evidence, and deterministic reasons.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w251_policy_events import service

router = APIRouter(tags=["Policy Events v1"])

@router.get("/api/policy-events")
async def api_policy_events_w251_list_events(limit: int = 100):
    """List policy events"""
    items = service.list_events(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/policy-events", status_code=201)
async def api_policy_events_w251_create_event(request: Request):
    """Create policy event"""
    data = await request.json()
    item = service.create_event(data)
    return item

@router.get("/api/policy-events/report")
async def api_policy_events_w251_event_report(limit: int = 100):
    """Get policy events report"""
    items = service.event_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/policy-events/{event_id}")
async def api_policy_events_w251_get_event(event_id: str):
    """Get policy event details"""
    item = service.get_event(event_id)
    if not item:
        raise HTTPException(status_code=404, detail="policy_events not found")
    return item

@router.post("/api/policy-events/{event_id}/classify")
async def api_policy_events_w251_classify_event(event_id: str, request: Request):
    """Classify policy event"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.classify_event(event_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_events not found")
    return item

@router.post("/api/policy-events/{event_id}/evidence")
async def api_policy_events_w251_link_evidence(event_id: str, request: Request):
    """Link evidence to event"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_evidence(event_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_events not found")
    return item
