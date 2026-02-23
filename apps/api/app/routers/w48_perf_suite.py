"""Wave 48: Performance Suite 2.0 Router — Large deterministic fixtures, perf budgets, query indexes, 10x scale testing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w48_perf_suite import service

router = APIRouter(tags=["Performance Suite 2.0"])

@router.get("/api/perf-suite/benchmarks")
async def api_perf_suite_w48_list_benchmarks(limit: int = 100):
    """List performance benchmarks"""
    items = service.list_benchmarks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/perf-suite/benchmarks", status_code=201)
async def api_perf_suite_w48_run_benchmark(request: Request):
    """Run a performance benchmark"""
    data = await request.json()
    item = service.run_benchmark(data)
    return item

@router.get("/api/perf-suite/compare")
async def api_perf_suite_w48_compare(limit: int = 100):
    """Compare benchmark runs"""
    items = service.compare(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/perf-suite/regression")
async def api_perf_suite_w48_regression_gate(limit: int = 100):
    """Check regression gate"""
    items = service.regression_gate(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/perf-suite/benchmarks/{benchmark_id}")
async def api_perf_suite_w48_get_benchmark(benchmark_id: str):
    """Get benchmark details"""
    item = service.get_benchmark(benchmark_id)
    if not item:
        raise HTTPException(status_code=404, detail="perf_suite not found")
    return item

@router.post("/api/perf-suite/benchmarks/{benchmark_id}/budget")
async def api_perf_suite_w48_set_budget(benchmark_id: str, request: Request):
    """Set performance budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_budget(benchmark_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_suite not found")
    return item
