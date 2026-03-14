"""Wave 86: Multi-Entity Close Calendar Router — Cross-entity close calendar dependencies with entity-level SLAs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w086_multi_entity_cal import service

router = APIRouter(tags=["Multi-Entity Close Calendar"])

@router.get("/api/multi-entity-cal")
async def api_multi_entity_cal_w86_list_calendars(limit: int = 100):
    """List multi-entity calendars"""
    items = service.list_calendars(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/multi-entity-cal", status_code=201)
async def api_multi_entity_cal_w86_create_calendar(request: Request):
    """Create multi-entity calendar"""
    data = await request.json()
    item = service.create_calendar(data)
    return item

@router.get("/api/multi-entity-cal/report")
async def api_multi_entity_cal_w86_cross_entity_report(limit: int = 100):
    """Get cross-entity report"""
    items = service.cross_entity_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/multi-entity-cal/{cal_id}")
async def api_multi_entity_cal_w86_get_calendar(cal_id: str):
    """Get calendar details"""
    item = service.get_calendar(cal_id)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_cal not found")
    return item

@router.post("/api/multi-entity-cal/{cal_id}/progress")
async def api_multi_entity_cal_w86_progress(cal_id: str, request: Request):
    """Update progress"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.progress(cal_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_cal not found")
    return item

@router.post("/api/multi-entity-cal/{cal_id}/sync")
async def api_multi_entity_cal_w86_sync_deps(cal_id: str, request: Request):
    """Sync entity dependencies"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sync_deps(cal_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_cal not found")
    return item
