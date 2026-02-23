"""Wave 117: Data Performance 25x Router — Performance suite with 25x fixtures for data export operations.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w117_data_perf_25x import service

router = APIRouter(tags=["Data Performance 25x"])

@router.get("/api/data-perf-25x")
async def api_data_perf_25x_w117_list_benchmarks(limit: int = 100):
    """List 25x perf benchmarks"""
    items = service.list_benchmarks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/data-perf-25x", status_code=201)
async def api_data_perf_25x_w117_run_benchmark(request: Request):
    """Run 25x perf benchmark"""
    data = await request.json()
    item = service.run_benchmark(data)
    return item

@router.get("/api/data-perf-25x/report")
async def api_data_perf_25x_w117_perf_report(limit: int = 100):
    """Get 25x perf report"""
    items = service.perf_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-perf-25x/{perf_id}")
async def api_data_perf_25x_w117_get_benchmark(perf_id: str):
    """Get benchmark details"""
    item = service.get_benchmark(perf_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_perf_25x not found")
    return item

@router.post("/api/data-perf-25x/{perf_id}/budget")
async def api_data_perf_25x_w117_set_budget(perf_id: str, request: Request):
    """Set perf budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_budget(perf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_perf_25x not found")
    return item
