"""Wave 28: Judge Demo Harness Router — Demo judge for LLM evaluation of extraction quality.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w28_judge_demo import service

router = APIRouter(tags=["Judge Demo Harness"])

@router.post("/api/judge/batch", status_code=201)
async def api_batch(request: Request):
    """Batch evaluation"""
    data = await request.json()
    item = service.batch(data)
    return item

@router.post("/api/judge/evaluate", status_code=201)
async def api_evaluate(request: Request):
    """Run judge evaluation"""
    data = await request.json()
    item = service.evaluate(data)
    return item

@router.get("/api/judge/leaderboard")
async def api_leaderboard(limit: int = 100):
    """Judge leaderboard"""
    items = service.leaderboard(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/judge/runs")
async def api_list(limit: int = 100):
    """List judge runs"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/judge/runs/{judge_id}")
async def api_get(judge_id: str):
    """Get judge result"""
    item = service.get(judge_id)
    if not item:
        raise HTTPException(status_code=404, detail="judge_demo not found")
    return item
