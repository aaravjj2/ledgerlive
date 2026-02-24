"""Wave 265: Replay Regression Harness v2 Router — Multiple canonical closes re-run offline and drift diffs captured deterministically. Regression harness with budgeted drift tolerance.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w265_replay_regression import service

router = APIRouter(tags=["Replay Regression Harness v2"])

@router.get("/api/replay-regression")
async def api_replay_regression_w265_list_harnesses(limit: int = 100):
    """List replay regression harnesses"""
    items = service.list_harnesses(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-regression", status_code=201)
async def api_replay_regression_w265_create_harness(request: Request):
    """Create regression harness"""
    data = await request.json()
    item = service.create_harness(data)
    return item

@router.get("/api/replay-regression/report")
async def api_replay_regression_w265_harness_report(limit: int = 100):
    """Get regression harness report"""
    items = service.harness_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-regression/{harness_id}")
async def api_replay_regression_w265_get_harness(harness_id: str):
    """Get harness details"""
    item = service.get_harness(harness_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_regression not found")
    return item

@router.post("/api/replay-regression/{harness_id}/drift")
async def api_replay_regression_w265_compare_drift(harness_id: str, request: Request):
    """Compare drift against budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare_drift(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_regression not found")
    return item

@router.post("/api/replay-regression/{harness_id}/run")
async def api_replay_regression_w265_run_regression(harness_id: str, request: Request):
    """Run regression suite"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_regression(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_regression not found")
    return item
