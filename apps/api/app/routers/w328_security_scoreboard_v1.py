"""Wave 328: Security Scoreboard v1 Router — Blocked actions, reasons, remediation success rate; deterministic metrics.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w328_security_scoreboard_v1 import service

router = APIRouter(tags=["Security Scoreboard v1"])

@router.get("/api/security-scoreboard-v1")
async def api_security_scoreboard_v1_w328_list_scores(limit: int = 100):
    """List security scores"""
    items = service.list_scores(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-scoreboard-v1", status_code=201)
async def api_security_scoreboard_v1_w328_create_score(request: Request):
    """Create security score"""
    data = await request.json()
    item = service.create_score(data)
    return item

@router.get("/api/security-scoreboard-v1/report")
async def api_security_scoreboard_v1_w328_score_report(limit: int = 100):
    """Get security scoreboard report"""
    items = service.score_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-scoreboard-v1/{score_id}")
async def api_security_scoreboard_v1_w328_get_score(score_id: str):
    """Get score details"""
    item = service.get_score(score_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_scoreboard_v1 not found")
    return item

@router.post("/api/security-scoreboard-v1/{score_id}/export")
async def api_security_scoreboard_v1_w328_export_metrics(score_id: str, request: Request):
    """Export metrics"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_metrics(score_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_scoreboard_v1 not found")
    return item

@router.post("/api/security-scoreboard-v1/{score_id}/recalculate")
async def api_security_scoreboard_v1_w328_recalculate(score_id: str, request: Request):
    """Recalculate score"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recalculate(score_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_scoreboard_v1 not found")
    return item
