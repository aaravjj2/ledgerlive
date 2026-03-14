"""Wave 103: eDiscovery Workflows 3.0 Router — Legal holds, approvals, and scoped exports for eDiscovery compliance.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w103_ediscovery import service

router = APIRouter(tags=["eDiscovery Workflows 3.0"])

@router.get("/api/ediscovery/holds")
async def api_ediscovery_w103_list_holds(limit: int = 100):
    """List legal holds"""
    items = service.list_holds(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ediscovery/holds", status_code=201)
async def api_ediscovery_w103_create_hold(request: Request):
    """Create legal hold"""
    data = await request.json()
    item = service.create_hold(data)
    return item

@router.get("/api/ediscovery/report")
async def api_ediscovery_w103_hold_report(limit: int = 100):
    """Get eDiscovery report"""
    items = service.hold_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ediscovery/holds/{hold_id}")
async def api_ediscovery_w103_get_hold(hold_id: str):
    """Get hold details"""
    item = service.get_hold(hold_id)
    if not item:
        raise HTTPException(status_code=404, detail="ediscovery not found")
    return item

@router.post("/api/ediscovery/holds/{hold_id}/approve")
async def api_ediscovery_w103_approve_hold(hold_id: str, request: Request):
    """Approve legal hold"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_hold(hold_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ediscovery not found")
    return item

@router.post("/api/ediscovery/holds/{hold_id}/export")
async def api_ediscovery_w103_scope_export(hold_id: str, request: Request):
    """Create scoped export"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.scope_export(hold_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ediscovery not found")
    return item

@router.post("/api/ediscovery/holds/{hold_id}/release")
async def api_ediscovery_w103_release_hold(hold_id: str, request: Request):
    """Release legal hold"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.release_hold(hold_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ediscovery not found")
    return item
