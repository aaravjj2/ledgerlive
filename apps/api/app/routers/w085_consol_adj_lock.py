"""Wave 85: Consolidation Adjustments Lock Router — Consolidation adjustments with approval workflow and lock enforcement.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w085_consol_adj_lock import service

router = APIRouter(tags=["Consolidation Adjustments Lock"])

@router.get("/api/consol-adj-locks")
async def api_consol_adj_lock_w85_list_adjustments(limit: int = 100):
    """List adjustments with locks"""
    items = service.list_adjustments(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/consol-adj-locks", status_code=201)
async def api_consol_adj_lock_w85_create_adjustment(request: Request):
    """Create adjustment"""
    data = await request.json()
    item = service.create_adjustment(data)
    return item

@router.get("/api/consol-adj-locks/report")
async def api_consol_adj_lock_w85_adj_report(limit: int = 100):
    """Get adjustments report"""
    items = service.adj_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/consol-adj-locks/{adj_id}")
async def api_consol_adj_lock_w85_get_adjustment(adj_id: str):
    """Get adjustment details"""
    item = service.get_adjustment(adj_id)
    if not item:
        raise HTTPException(status_code=404, detail="consol_adj_lock not found")
    return item

@router.post("/api/consol-adj-locks/{adj_id}/approve")
async def api_consol_adj_lock_w85_approve(adj_id: str, request: Request):
    """Approve adjustment"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve(adj_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_adj_lock not found")
    return item

@router.post("/api/consol-adj-locks/{adj_id}/deny")
async def api_consol_adj_lock_w85_deny_after_lock(adj_id: str, request: Request):
    """Deny post-lock modification"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deny_after_lock(adj_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_adj_lock not found")
    return item

@router.post("/api/consol-adj-locks/{adj_id}/lock")
async def api_consol_adj_lock_w85_lock_adj(adj_id: str, request: Request):
    """Lock adjustment"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.lock_adj(adj_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_adj_lock not found")
    return item
