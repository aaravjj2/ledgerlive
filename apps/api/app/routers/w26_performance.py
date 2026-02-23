"""Wave 26: Performance Monitor Router — API performance tracking, latency histograms, and chaos flags.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w26_performance import service

router = APIRouter(tags=["Performance Monitor"])

@router.get("/api/performance/metrics")
async def api_list_metrics(limit: int = 100):
    """Get performance metrics"""
    items = service.list_metrics(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/performance/metrics", status_code=201)
async def api_create_metric(request: Request):
    """Record a performance metric"""
    data = await request.json()
    item = service.create_metric(data)
    return item

@router.get("/api/performance/metrics/{metric_id}")
async def api_get_metric(metric_id: str):
    """Get metric details"""
    item = service.get_metric(metric_id)
    if not item:
        raise HTTPException(status_code=404, detail="performance not found")
    return item

@router.post("/api/performance/metrics/{metric_id}/chaos")
async def api_chaos_flag(metric_id: str, request: Request):
    """Set chaos testing flag"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.chaos_flag(metric_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="performance not found")
    return item

@router.post("/api/performance/metrics/{metric_id}/clear")
async def api_clear_metrics(metric_id: str, request: Request):
    """Clear metrics"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.clear_metrics(metric_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="performance not found")
    return item
