"""Wave 75: Triage Queue 2.0 Router — Exception triage queue with escalation policies and frozen-time simulation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w075_triage_queue_v2 import service

router = APIRouter(tags=["Triage Queue 2.0"])

@router.get("/api/triage-queue-v2")
async def api_triage_queue_v2_w75_list_queue(limit: int = 100):
    """List triage queue"""
    items = service.list_queue(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/triage-queue-v2", status_code=201)
async def api_triage_queue_v2_w75_add_to_queue(request: Request):
    """Add exception to triage queue"""
    data = await request.json()
    item = service.add_to_queue(data)
    return item

@router.get("/api/triage-queue-v2/sla-report")
async def api_triage_queue_v2_w75_sla_report(limit: int = 100):
    """Get SLA compliance report"""
    items = service.sla_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/triage-queue-v2/stats")
async def api_triage_queue_v2_w75_queue_stats(limit: int = 100):
    """Get queue statistics"""
    items = service.queue_stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/triage-queue-v2/{triage_id}")
async def api_triage_queue_v2_w75_get_triage(triage_id: str):
    """Get triage item details"""
    item = service.get_triage(triage_id)
    if not item:
        raise HTTPException(status_code=404, detail="triage_queue_v2 not found")
    return item

@router.post("/api/triage-queue-v2/{triage_id}/escalate")
async def api_triage_queue_v2_w75_escalate(triage_id: str, request: Request):
    """Escalate triage item"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.escalate(triage_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="triage_queue_v2 not found")
    return item

@router.post("/api/triage-queue-v2/{triage_id}/resolve")
async def api_triage_queue_v2_w75_resolve(triage_id: str, request: Request):
    """Resolve triage item"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve(triage_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="triage_queue_v2 not found")
    return item
