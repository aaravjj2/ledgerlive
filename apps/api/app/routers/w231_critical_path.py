"""Wave 231: Critical Path Analyzer v1 Router — Identifies the critical path through the close task DAG. Computes earliest/latest start and finish times, float values, and bottleneck nodes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w231_critical_path import service

router = APIRouter(tags=["Critical Path Analyzer v1"])

@router.get("/api/critical-path")
async def api_critical_path_w231_list_analyses(limit: int = 100):
    """List critical path analyses"""
    items = service.list_analyses(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/critical-path", status_code=201)
async def api_critical_path_w231_analyze_path(request: Request):
    """Analyze critical path"""
    data = await request.json()
    item = service.analyze_path(data)
    return item

@router.get("/api/critical-path/report")
async def api_critical_path_w231_path_report(limit: int = 100):
    """Get critical path report"""
    items = service.path_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/critical-path/{analysis_id}")
async def api_critical_path_w231_get_analysis(analysis_id: str):
    """Get analysis details"""
    item = service.get_analysis(analysis_id)
    if not item:
        raise HTTPException(status_code=404, detail="critical_path not found")
    return item

@router.post("/api/critical-path/{analysis_id}/bottleneck")
async def api_critical_path_w231_find_bottleneck(analysis_id: str, request: Request):
    """Find bottleneck node"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.find_bottleneck(analysis_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="critical_path not found")
    return item

@router.post("/api/critical-path/{analysis_id}/float")
async def api_critical_path_w231_compute_float(analysis_id: str, request: Request):
    """Compute float values"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compute_float(analysis_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="critical_path not found")
    return item
