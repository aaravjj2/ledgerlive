"""Wave 1: Close Period Management Router — Manage accounting close periods with open/close/lock lifecycle.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w01_close_period import service

router = APIRouter(tags=["Close Period Management"])

@router.get("/api/close-periods")
async def api_list(limit: int = 100):
    """List all close periods"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-periods", status_code=201)
async def api_create(request: Request):
    """Create a new close period"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/close-periods/{period_id}")
async def api_get(period_id: str):
    """Get a close period by ID"""
    item = service.get(period_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_period not found")
    return item

@router.post("/api/close-periods/{period_id}/close")
async def api_close_period(period_id: str, request: Request):
    """Close a period"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.close_period(period_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_period not found")
    return item

@router.post("/api/close-periods/{period_id}/lock")
async def api_lock_period(period_id: str, request: Request):
    """Lock a period"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.lock_period(period_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_period not found")
    return item
