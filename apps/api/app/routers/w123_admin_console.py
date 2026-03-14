"""Wave 123: Policy Admin Console Router — Admin console for ABAC policies with full audit trails.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w123_admin_console import service

router = APIRouter(tags=["Policy Admin Console"])

@router.get("/api/admin-console")
async def api_admin_console_w123_list_actions(limit: int = 100):
    """List admin actions"""
    items = service.list_actions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/admin-console", status_code=201)
async def api_admin_console_w123_perform_action(request: Request):
    """Perform admin action"""
    data = await request.json()
    item = service.perform_action(data)
    return item

@router.get("/api/admin-console/audit")
async def api_admin_console_w123_audit_log(limit: int = 100):
    """Get admin audit log"""
    items = service.audit_log(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/admin-console/report")
async def api_admin_console_w123_action_report(limit: int = 100):
    """Get admin action report"""
    items = service.action_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/admin-console/{action_id}")
async def api_admin_console_w123_get_action(action_id: str):
    """Get action details"""
    item = service.get_action(action_id)
    if not item:
        raise HTTPException(status_code=404, detail="admin_console not found")
    return item

@router.post("/api/admin-console/{action_id}/revert")
async def api_admin_console_w123_revert_action(action_id: str, request: Request):
    """Revert admin action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.revert_action(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="admin_console not found")
    return item
