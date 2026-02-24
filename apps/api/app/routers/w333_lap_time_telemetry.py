"""Wave 333: Lap Time Telemetry v1 Router — Deterministic durations per step (bucketed), critical path heatmap.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w333_lap_time_telemetry import service

router = APIRouter(tags=["Lap Time Telemetry v1"])

@router.get("/api/lap-time-telemetry")
async def api_lap_time_telemetry_w333_list_laps(limit: int = 100):
    """List lap times"""
    items = service.list_laps(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/lap-time-telemetry", status_code=201)
async def api_lap_time_telemetry_w333_record_lap(request: Request):
    """Record lap time"""
    data = await request.json()
    item = service.record_lap(data)
    return item

@router.get("/api/lap-time-telemetry/report")
async def api_lap_time_telemetry_w333_lap_report(limit: int = 100):
    """Get lap time report"""
    items = service.lap_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/lap-time-telemetry/{lap_id}")
async def api_lap_time_telemetry_w333_get_lap(lap_id: str):
    """Get lap details"""
    item = service.get_lap(lap_id)
    if not item:
        raise HTTPException(status_code=404, detail="lap_time_telemetry not found")
    return item

@router.post("/api/lap-time-telemetry/{lap_id}/bucket")
async def api_lap_time_telemetry_w333_bucket_analysis(lap_id: str, request: Request):
    """Run bucket analysis"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.bucket_analysis(lap_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="lap_time_telemetry not found")
    return item

@router.post("/api/lap-time-telemetry/{lap_id}/heatmap")
async def api_lap_time_telemetry_w333_heatmap_data(lap_id: str, request: Request):
    """Generate heatmap data"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.heatmap_data(lap_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="lap_time_telemetry not found")
    return item
