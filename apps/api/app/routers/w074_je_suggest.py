"""Wave 74: JE Suggestion Engine Router — Journal entry suggestions tied to controls and approvals with evidence links.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w074_je_suggest import service

router = APIRouter(tags=["JE Suggestion Engine"])

@router.get("/api/je-suggestions")
async def api_je_suggest_w74_list_suggestions(limit: int = 100):
    """List JE suggestions"""
    items = service.list_suggestions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/je-suggestions", status_code=201)
async def api_je_suggest_w74_generate(request: Request):
    """Generate JE suggestions"""
    data = await request.json()
    item = service.generate(data)
    return item

@router.get("/api/je-suggestions/report")
async def api_je_suggest_w74_suggestion_report(limit: int = 100):
    """Get suggestion report"""
    items = service.suggestion_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/je-suggestions/{suggestion_id}")
async def api_je_suggest_w74_get_suggestion(suggestion_id: str):
    """Get suggestion details"""
    item = service.get_suggestion(suggestion_id)
    if not item:
        raise HTTPException(status_code=404, detail="je_suggest not found")
    return item

@router.post("/api/je-suggestions/{suggestion_id}/approve")
async def api_je_suggest_w74_approve(suggestion_id: str, request: Request):
    """Approve suggestion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve(suggestion_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_suggest not found")
    return item

@router.post("/api/je-suggestions/{suggestion_id}/post")
async def api_je_suggest_w74_post_je(suggestion_id: str, request: Request):
    """Post approved JE"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.post_je(suggestion_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_suggest not found")
    return item

@router.post("/api/je-suggestions/{suggestion_id}/reject")
async def api_je_suggest_w74_reject(suggestion_id: str, request: Request):
    """Reject suggestion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject(suggestion_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_suggest not found")
    return item
