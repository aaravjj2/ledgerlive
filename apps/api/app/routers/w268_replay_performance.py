"""Wave 268: Replay Performance v1 Router — 10x and 25x fixture replays with enforced performance budgets. Stable pagination and deterministic replay timing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w268_replay_performance import service

router = APIRouter(tags=["Replay Performance v1"])

@router.get("/api/replay-performance")
async def api_replay_performance_w268_list_perfs(limit: int = 100):
    """List replay performance tests"""
    items = service.list_perfs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-performance", status_code=201)
async def api_replay_performance_w268_run_perf_test(request: Request):
    """Run replay performance test"""
    data = await request.json()
    item = service.run_perf_test(data)
    return item

@router.get("/api/replay-performance/report")
async def api_replay_performance_w268_perf_report(limit: int = 100):
    """Get replay performance report"""
    items = service.perf_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-performance/{perf_id}")
async def api_replay_performance_w268_get_perf(perf_id: str):
    """Get performance test details"""
    item = service.get_perf(perf_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_performance not found")
    return item

@router.post("/api/replay-performance/{perf_id}/run-10x")
async def api_replay_performance_w268_run_10x(perf_id: str, request: Request):
    """Run 10x fixture replay"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_10x(perf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_performance not found")
    return item

@router.post("/api/replay-performance/{perf_id}/run-25x")
async def api_replay_performance_w268_run_25x(perf_id: str, request: Request):
    """Run 25x fixture replay"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_25x(perf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_performance not found")
    return item
