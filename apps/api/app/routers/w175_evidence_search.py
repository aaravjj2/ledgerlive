"""Wave 175: Evidence Graph Search v2 Router — Local offline index over docs, exceptions, tool traces, and audit with deterministic ordering, pagination, and saved searches.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w175_evidence_search import service

router = APIRouter(tags=["Evidence Graph Search v2"])

@router.get("/api/evidence-search")
async def api_evidence_search_w175_list_searches(limit: int = 100):
    """List saved searches"""
    items = service.list_searches(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/evidence-search", status_code=201)
async def api_evidence_search_w175_execute_search(request: Request):
    """Execute evidence search"""
    data = await request.json()
    item = service.execute_search(data)
    return item

@router.get("/api/evidence-search/report")
async def api_evidence_search_w175_search_report(limit: int = 100):
    """Get search report"""
    items = service.search_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/evidence-search/{search_id}")
async def api_evidence_search_w175_get_search(search_id: str):
    """Get search details"""
    item = service.get_search(search_id)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_search not found")
    return item

@router.post("/api/evidence-search/{search_id}/open")
async def api_evidence_search_w175_open_evidence(search_id: str, request: Request):
    """Open linked evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.open_evidence(search_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_search not found")
    return item

@router.post("/api/evidence-search/{search_id}/save")
async def api_evidence_search_w175_save_search(search_id: str, request: Request):
    """Save search for reuse"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.save_search(search_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_search not found")
    return item
