"""Wave 7: Exception Management Router — Taxonomy-based exception triage for reconciliation mismatches.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w07_exception import service

router = APIRouter(tags=["Exception Management"])

@router.get("/api/exceptions")
async def api_list(limit: int = 100):
    """List exceptions"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/exceptions", status_code=201)
async def api_create(request: Request):
    """Create an exception"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/exceptions/{exception_id}")
async def api_get(exception_id: str):
    """Get exception details"""
    item = service.get(exception_id)
    if not item:
        raise HTTPException(status_code=404, detail="exception not found")
    return item

@router.post("/api/exceptions/{exception_id}/assign")
async def api_assign(exception_id: str, request: Request):
    """Assign exception"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assign(exception_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exception not found")
    return item

@router.post("/api/exceptions/{exception_id}/resolve")
async def api_resolve(exception_id: str, request: Request):
    """Resolve exception"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve(exception_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exception not found")
    return item
