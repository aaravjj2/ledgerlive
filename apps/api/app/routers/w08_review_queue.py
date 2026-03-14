"""Wave 8: HITL Review Queue Router — Human-in-the-loop review and approval workflow.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w08_review_queue import service

router = APIRouter(tags=["HITL Review Queue"])

@router.get("/api/reviews")
async def api_list(limit: int = 100):
    """List review items"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/reviews", status_code=201)
async def api_enqueue(request: Request):
    """Add item to review queue"""
    data = await request.json()
    item = service.enqueue(data)
    return item

@router.get("/api/reviews/stats")
async def api_stats(limit: int = 100):
    """Review queue statistics"""
    items = service.stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/reviews/{review_id}")
async def api_get(review_id: str):
    """Get review details"""
    item = service.get(review_id)
    if not item:
        raise HTTPException(status_code=404, detail="review_queue not found")
    return item

@router.post("/api/reviews/{review_id}/decide")
async def api_decide(review_id: str, request: Request):
    """Submit review decision"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.decide(review_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="review_queue not found")
    return item
