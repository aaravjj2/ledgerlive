"""Wave 230: Lane Status Board v1 Router — Visual lane board showing close workstreams as swim lanes. Each lane has tasks ordered by dependency, colored by status, with live completion tracking.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w230_lane_status import service

router = APIRouter(tags=["Lane Status Board v1"])

@router.get("/api/lane-status")
async def api_lane_status_w230_list_lanes(limit: int = 100):
    """List lanes"""
    items = service.list_lanes(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/lane-status", status_code=201)
async def api_lane_status_w230_create_lane(request: Request):
    """Create lane"""
    data = await request.json()
    item = service.create_lane(data)
    return item

@router.get("/api/lane-status/report")
async def api_lane_status_w230_lane_report(limit: int = 100):
    """Get lane status report"""
    items = service.lane_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/lane-status/{lane_id}")
async def api_lane_status_w230_get_lane(lane_id: str):
    """Get lane details"""
    item = service.get_lane(lane_id)
    if not item:
        raise HTTPException(status_code=404, detail="lane_status not found")
    return item

@router.post("/api/lane-status/{lane_id}/reorder")
async def api_lane_status_w230_reorder_lane(lane_id: str, request: Request):
    """Reorder lane"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reorder_lane(lane_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="lane_status not found")
    return item

@router.post("/api/lane-status/{lane_id}/update")
async def api_lane_status_w230_update_lane(lane_id: str, request: Request):
    """Update lane status"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.update_lane(lane_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="lane_status not found")
    return item
