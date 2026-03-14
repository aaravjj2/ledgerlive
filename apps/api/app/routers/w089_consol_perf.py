"""Wave 89: Consolidation Performance Router — Performance pass for consolidation on 10x fixtures with timing budgets.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w089_consol_perf import service

router = APIRouter(tags=["Consolidation Performance"])

@router.get("/api/consol-perf")
async def api_consol_perf_w89_list_benchmarks(limit: int = 100):
    """List consolidation perf benchmarks"""
    items = service.list_benchmarks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/consol-perf", status_code=201)
async def api_consol_perf_w89_run_benchmark(request: Request):
    """Run consolidation perf benchmark"""
    data = await request.json()
    item = service.run_benchmark(data)
    return item

@router.get("/api/consol-perf/report")
async def api_consol_perf_w89_perf_report(limit: int = 100):
    """Get performance report"""
    items = service.perf_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/consol-perf/{perf_id}")
async def api_consol_perf_w89_get_benchmark(perf_id: str):
    """Get benchmark details"""
    item = service.get_benchmark(perf_id)
    if not item:
        raise HTTPException(status_code=404, detail="consol_perf not found")
    return item

@router.post("/api/consol-perf/{perf_id}/budget")
async def api_consol_perf_w89_set_budget(perf_id: str, request: Request):
    """Set perf budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_budget(perf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_perf not found")
    return item
