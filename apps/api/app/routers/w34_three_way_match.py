"""Wave 34: Three-Way Match Router — PO/Receipt/Invoice matching with tolerances, variance policy, and approval for out-of-range.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w34_three_way_match import service

router = APIRouter(tags=["Three-Way Match"])

@router.get("/api/three-way-match")
async def api_three_way_match_w34_list_matches(limit: int = 100):
    """List three-way matches"""
    items = service.list_matches(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/three-way-match", status_code=201)
async def api_three_way_match_w34_create_match(request: Request):
    """Create a three-way match"""
    data = await request.json()
    item = service.create_match(data)
    return item

@router.get("/api/three-way-match/{match_id}")
async def api_three_way_match_w34_get_match(match_id: str):
    """Get match details"""
    item = service.get_match(match_id)
    if not item:
        raise HTTPException(status_code=404, detail="three_way_match not found")
    return item

@router.post("/api/three-way-match/{match_id}/approve")
async def api_three_way_match_w34_approve_variance(match_id: str, request: Request):
    """Approve variance"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_variance(match_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="three_way_match not found")
    return item

@router.post("/api/three-way-match/{match_id}/recalculate")
async def api_three_way_match_w34_recalculate(match_id: str, request: Request):
    """Recalculate match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recalculate(match_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="three_way_match not found")
    return item

@router.post("/api/three-way-match/{match_id}/reject")
async def api_three_way_match_w34_reject_match(match_id: str, request: Request):
    """Reject a match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject_match(match_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="three_way_match not found")
    return item
