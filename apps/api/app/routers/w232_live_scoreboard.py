"""Wave 232: Live Scoreboard v1 Router — Real-time scoreboard displaying team progress, SLA adherence, blocker counts, and checkpoint completion. Auto-refreshing metrics with trend indicators.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w232_live_scoreboard import service

router = APIRouter(tags=["Live Scoreboard v1"])

@router.get("/api/live-scoreboard")
async def api_live_scoreboard_w232_list_scores(limit: int = 100):
    """List scoreboard snapshots"""
    items = service.list_scores(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/live-scoreboard", status_code=201)
async def api_live_scoreboard_w232_create_score(request: Request):
    """Create scoreboard snapshot"""
    data = await request.json()
    item = service.create_score(data)
    return item

@router.get("/api/live-scoreboard/report")
async def api_live_scoreboard_w232_scoreboard_report(limit: int = 100):
    """Get scoreboard report"""
    items = service.scoreboard_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/live-scoreboard/{score_id}")
async def api_live_scoreboard_w232_get_score(score_id: str):
    """Get scoreboard details"""
    item = service.get_score(score_id)
    if not item:
        raise HTTPException(status_code=404, detail="live_scoreboard not found")
    return item

@router.post("/api/live-scoreboard/{score_id}/rank")
async def api_live_scoreboard_w232_rank_teams(score_id: str, request: Request):
    """Rank teams by progress"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rank_teams(score_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="live_scoreboard not found")
    return item

@router.post("/api/live-scoreboard/{score_id}/refresh")
async def api_live_scoreboard_w232_refresh_score(score_id: str, request: Request):
    """Refresh scoreboard data"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.refresh_score(score_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="live_scoreboard not found")
    return item
