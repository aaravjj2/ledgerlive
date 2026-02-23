"""Wave 78: Close KPI Scorecard Router — Deterministic scorecard: coverage, exceptions, approvals, timeliness metrics.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w078_close_scorecard import service

router = APIRouter(tags=["Close KPI Scorecard"])

@router.get("/api/close-scorecards")
async def api_close_scorecard_w78_list_scorecards(limit: int = 100):
    """List close scorecards"""
    items = service.list_scorecards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-scorecards", status_code=201)
async def api_close_scorecard_w78_compute(request: Request):
    """Compute close scorecard"""
    data = await request.json()
    item = service.compute(data)
    return item

@router.get("/api/close-scorecards/export")
async def api_close_scorecard_w78_export_scorecard(limit: int = 100):
    """Export scorecard report"""
    items = service.export_scorecard(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-scorecards/trends")
async def api_close_scorecard_w78_trends(limit: int = 100):
    """Get scorecard trends"""
    items = service.trends(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-scorecards/{scorecard_id}")
async def api_close_scorecard_w78_get_scorecard(scorecard_id: str):
    """Get scorecard details"""
    item = service.get_scorecard(scorecard_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_scorecard not found")
    return item

@router.post("/api/close-scorecards/{scorecard_id}/drilldown")
async def api_close_scorecard_w78_drill_down(scorecard_id: str, request: Request):
    """Drill down into scorecard"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.drill_down(scorecard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_scorecard not found")
    return item
