"""Wave 33: JE Posting Engine Router — Journal entry batching, posting locks after close, reversals, and approval chain.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w33_je_posting import service

router = APIRouter(tags=["JE Posting Engine"])

@router.get("/api/je-postings")
async def api_je_posting_w33_list_postings(limit: int = 100):
    """List JE postings"""
    items = service.list_postings(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/je-postings", status_code=201)
async def api_je_posting_w33_create_posting(request: Request):
    """Create a JE posting batch"""
    data = await request.json()
    item = service.create_posting(data)
    return item

@router.get("/api/je-postings/{posting_id}")
async def api_je_posting_w33_get_posting(posting_id: str):
    """Get posting details"""
    item = service.get_posting(posting_id)
    if not item:
        raise HTTPException(status_code=404, detail="je_posting not found")
    return item

@router.post("/api/je-postings/{posting_id}/approve")
async def api_je_posting_w33_approve(posting_id: str, request: Request):
    """Approve a posting"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve(posting_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_posting not found")
    return item

@router.post("/api/je-postings/{posting_id}/lock")
async def api_je_posting_w33_lock(posting_id: str, request: Request):
    """Lock posting after close"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.lock(posting_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_posting not found")
    return item

@router.post("/api/je-postings/{posting_id}/post")
async def api_je_posting_w33_post(posting_id: str, request: Request):
    """Post the batch"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.post(posting_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_posting not found")
    return item

@router.post("/api/je-postings/{posting_id}/reverse")
async def api_je_posting_w33_reverse(posting_id: str, request: Request):
    """Create a reversal"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reverse(posting_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="je_posting not found")
    return item
