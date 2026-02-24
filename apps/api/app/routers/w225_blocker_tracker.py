"""Wave 225: Blocker Tracker v1 Router — Tracks blockers preventing close task completion. Categorizes blockers by type (data, approval, system), assigns owners, and tracks resolution workflow.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w225_blocker_tracker import service

router = APIRouter(tags=["Blocker Tracker v1"])

@router.get("/api/blocker-tracker")
async def api_blocker_tracker_w225_list_blockers(limit: int = 100):
    """List blockers"""
    items = service.list_blockers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/blocker-tracker", status_code=201)
async def api_blocker_tracker_w225_create_blocker(request: Request):
    """Create blocker"""
    data = await request.json()
    item = service.create_blocker(data)
    return item

@router.get("/api/blocker-tracker/report")
async def api_blocker_tracker_w225_blocker_report(limit: int = 100):
    """Get blocker tracker report"""
    items = service.blocker_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/blocker-tracker/{blocker_id}")
async def api_blocker_tracker_w225_get_blocker(blocker_id: str):
    """Get blocker details"""
    item = service.get_blocker(blocker_id)
    if not item:
        raise HTTPException(status_code=404, detail="blocker_tracker not found")
    return item

@router.post("/api/blocker-tracker/{blocker_id}/escalate")
async def api_blocker_tracker_w225_escalate_blocker(blocker_id: str, request: Request):
    """Escalate blocker"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.escalate_blocker(blocker_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blocker_tracker not found")
    return item

@router.post("/api/blocker-tracker/{blocker_id}/resolve")
async def api_blocker_tracker_w225_resolve_blocker(blocker_id: str, request: Request):
    """Resolve blocker"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve_blocker(blocker_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blocker_tracker not found")
    return item
