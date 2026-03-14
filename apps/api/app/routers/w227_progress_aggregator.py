"""Wave 227: Progress Aggregator v1 Router — Aggregates completion progress across all close tasks, DAG nodes, and team handoffs. Produces weighted progress percentage and phase-level breakdowns.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w227_progress_aggregator import service

router = APIRouter(tags=["Progress Aggregator v1"])

@router.get("/api/progress-aggregator")
async def api_progress_aggregator_w227_list_aggregations(limit: int = 100):
    """List progress aggregations"""
    items = service.list_aggregations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/progress-aggregator", status_code=201)
async def api_progress_aggregator_w227_aggregate(request: Request):
    """Compute progress aggregation"""
    data = await request.json()
    item = service.aggregate(data)
    return item

@router.get("/api/progress-aggregator/report")
async def api_progress_aggregator_w227_aggregator_report(limit: int = 100):
    """Get progress aggregator report"""
    items = service.aggregator_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/progress-aggregator/{aggregation_id}")
async def api_progress_aggregator_w227_get_aggregation(aggregation_id: str):
    """Get aggregation details"""
    item = service.get_aggregation(aggregation_id)
    if not item:
        raise HTTPException(status_code=404, detail="progress_aggregator not found")
    return item

@router.post("/api/progress-aggregator/{aggregation_id}/refresh")
async def api_progress_aggregator_w227_refresh(aggregation_id: str, request: Request):
    """Refresh aggregation data"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.refresh(aggregation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="progress_aggregator not found")
    return item

@router.post("/api/progress-aggregator/{aggregation_id}/team")
async def api_progress_aggregator_w227_team_detail(aggregation_id: str, request: Request):
    """Get team-level detail"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.team_detail(aggregation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="progress_aggregator not found")
    return item
