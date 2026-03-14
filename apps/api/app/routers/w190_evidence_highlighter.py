"""Wave 190: Evidence Span Highlighter v2 Router — Multi-page multi-field evidence viewer with deep links from tool trace to dossier. Highlights evidence correctly in viewer.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w190_evidence_highlighter import service

router = APIRouter(tags=["Evidence Span Highlighter v2"])

@router.get("/api/evidence-highlights")
async def api_evidence_highlighter_w190_list_highlights(limit: int = 100):
    """List evidence highlights"""
    items = service.list_highlights(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/evidence-highlights", status_code=201)
async def api_evidence_highlighter_w190_create_highlight(request: Request):
    """Create evidence highlight"""
    data = await request.json()
    item = service.create_highlight(data)
    return item

@router.get("/api/evidence-highlights/report")
async def api_evidence_highlighter_w190_highlight_report(limit: int = 100):
    """Get highlights report"""
    items = service.highlight_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/evidence-highlights/{highlight_id}")
async def api_evidence_highlighter_w190_get_highlight(highlight_id: str):
    """Get highlight details"""
    item = service.get_highlight(highlight_id)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_highlighter not found")
    return item

@router.post("/api/evidence-highlights/{highlight_id}/link")
async def api_evidence_highlighter_w190_link_to_dossier(highlight_id: str, request: Request):
    """Link highlight to dossier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_to_dossier(highlight_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_highlighter not found")
    return item

@router.post("/api/evidence-highlights/{highlight_id}/open")
async def api_evidence_highlighter_w190_open_deep_link(highlight_id: str, request: Request):
    """Open deep link from tool trace"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.open_deep_link(highlight_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_highlighter not found")
    return item
