"""Wave 202: Live Reconnect Buffering Resume v2 Router — Session buffering with deterministic replay of streamed events. Resume token model prevents duplicated tool calls on reconnect. Protocol schema versioning.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w202_live_reconnect import service

router = APIRouter(tags=["Live Reconnect Buffering Resume v2"])

@router.get("/api/live-reconnect")
async def api_live_reconnect_w202_list_reconnects(limit: int = 100):
    """List reconnect records"""
    items = service.list_reconnects(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/live-reconnect", status_code=201)
async def api_live_reconnect_w202_create_reconnect(request: Request):
    """Create reconnect session"""
    data = await request.json()
    item = service.create_reconnect(data)
    return item

@router.get("/api/live-reconnect/report")
async def api_live_reconnect_w202_reconnect_report(limit: int = 100):
    """Get reconnect report"""
    items = service.reconnect_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/live-reconnect/{reconnect_id}")
async def api_live_reconnect_w202_get_reconnect(reconnect_id: str):
    """Get reconnect details"""
    item = service.get_reconnect(reconnect_id)
    if not item:
        raise HTTPException(status_code=404, detail="live_reconnect not found")
    return item

@router.post("/api/live-reconnect/{reconnect_id}/buffer")
async def api_live_reconnect_w202_buffer_event(reconnect_id: str, request: Request):
    """Buffer a streamed event"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.buffer_event(reconnect_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="live_reconnect not found")
    return item

@router.post("/api/live-reconnect/{reconnect_id}/resume")
async def api_live_reconnect_w202_resume_session(reconnect_id: str, request: Request):
    """Resume session from token"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resume_session(reconnect_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="live_reconnect not found")
    return item

@router.post("/api/live-reconnect/{reconnect_id}/validate")
async def api_live_reconnect_w202_validate_protocol(reconnect_id: str, request: Request):
    """Validate protocol schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_protocol(reconnect_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="live_reconnect not found")
    return item
