"""Wave 221: Close Calendar Manager v1 Router — Manages financial close calendars with period definitions, milestone dates, and working-day calculations. Supports recurring close schedules and holiday-aware date math.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w221_close_calendar import service

router = APIRouter(tags=["Close Calendar Manager v1"])

@router.get("/api/period-calendar")
async def api_close_calendar_w221_list_calendars(limit: int = 100):
    """List close calendars"""
    items = service.list_calendars(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/period-calendar", status_code=201)
async def api_close_calendar_w221_create_calendar(request: Request):
    """Create close calendar period"""
    data = await request.json()
    item = service.create_calendar(data)
    return item

@router.get("/api/period-calendar/report")
async def api_close_calendar_w221_calendar_report(limit: int = 100):
    """Get calendar summary report"""
    items = service.calendar_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/period-calendar/{calendar_id}")
async def api_close_calendar_w221_get_calendar(calendar_id: str):
    """Get calendar details"""
    item = service.get_calendar(calendar_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item

@router.post("/api/period-calendar/{calendar_id}/advance")
async def api_close_calendar_w221_advance_day(calendar_id: str, request: Request):
    """Advance working day"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_day(calendar_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item

@router.post("/api/period-calendar/{calendar_id}/finalize")
async def api_close_calendar_w221_finalize_period(calendar_id: str, request: Request):
    """Finalize close period"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.finalize_period(calendar_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item

@router.post("/api/period-calendar/{calendar_id}/milestone")
async def api_close_calendar_w221_set_milestone(calendar_id: str, request: Request):
    """Set milestone date"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_milestone(calendar_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item
