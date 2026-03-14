"""Wave 158: No Drift Meta-Guards Router — Expanded no-drift meta-guards ensuring output stability across runs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w158_no_drift_guard import service

router = APIRouter(tags=["No Drift Meta-Guards"])

@router.get("/api/no-drift-guards")
async def api_no_drift_guard_w158_list_guards(limit: int = 100):
    """List no-drift guards"""
    items = service.list_guards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/no-drift-guards", status_code=201)
async def api_no_drift_guard_w158_set_baseline(request: Request):
    """Set drift baseline"""
    data = await request.json()
    item = service.set_baseline(data)
    return item

@router.get("/api/no-drift-guards/report")
async def api_no_drift_guard_w158_drift_report(limit: int = 100):
    """Get drift detection report"""
    items = service.drift_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/no-drift-guards/{guard_id}")
async def api_no_drift_guard_w158_get_guard(guard_id: str):
    """Get guard details"""
    item = service.get_guard(guard_id)
    if not item:
        raise HTTPException(status_code=404, detail="no_drift_guard not found")
    return item

@router.post("/api/no-drift-guards/{guard_id}/check")
async def api_no_drift_guard_w158_check_drift(guard_id: str, request: Request):
    """Check for drift"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_drift(guard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="no_drift_guard not found")
    return item
