"""Wave 73: Accrual Suggestion Engine Router — Pattern-based deterministic accrual suggestions with approve/post workflow.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w073_accrual_suggest import service

router = APIRouter(tags=["Accrual Suggestion Engine"])

@router.get("/api/accrual-suggestions")
async def api_accrual_suggest_w73_list_suggestions(limit: int = 100):
    """List accrual suggestions"""
    items = service.list_suggestions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/accrual-suggestions", status_code=201)
async def api_accrual_suggest_w73_generate(request: Request):
    """Generate accrual suggestions"""
    data = await request.json()
    item = service.generate(data)
    return item

@router.get("/api/accrual-suggestions/stats")
async def api_accrual_suggest_w73_suggestion_stats(limit: int = 100):
    """Get suggestion statistics"""
    items = service.suggestion_stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/accrual-suggestions/{suggestion_id}")
async def api_accrual_suggest_w73_get_suggestion(suggestion_id: str):
    """Get suggestion details"""
    item = service.get_suggestion(suggestion_id)
    if not item:
        raise HTTPException(status_code=404, detail="accrual_suggest not found")
    return item

@router.post("/api/accrual-suggestions/{suggestion_id}/approve")
async def api_accrual_suggest_w73_approve(suggestion_id: str, request: Request):
    """Approve suggestion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve(suggestion_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="accrual_suggest not found")
    return item

@router.post("/api/accrual-suggestions/{suggestion_id}/post")
async def api_accrual_suggest_w73_post_accrual(suggestion_id: str, request: Request):
    """Post approved accrual"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.post_accrual(suggestion_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="accrual_suggest not found")
    return item

@router.post("/api/accrual-suggestions/{suggestion_id}/reject")
async def api_accrual_suggest_w73_reject(suggestion_id: str, request: Request):
    """Reject suggestion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject(suggestion_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="accrual_suggest not found")
    return item
