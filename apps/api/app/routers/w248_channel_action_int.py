"""Wave 248: Channel Action Integration v1 Router — Approve or deny steps from mock chat/email cards. Updates plan state immediately with full audit trail and deterministic processing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w248_channel_action_int import service

router = APIRouter(tags=["Channel Action Integration v1"])

@router.get("/api/channel-action")
async def api_channel_action_int_w248_list_channel_actions(limit: int = 100):
    """List channel actions"""
    items = service.list_channel_actions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/channel-action", status_code=201)
async def api_channel_action_int_w248_create_channel_action(request: Request):
    """Create channel action"""
    data = await request.json()
    item = service.create_channel_action(data)
    return item

@router.get("/api/channel-action/report")
async def api_channel_action_int_w248_channel_action_report(limit: int = 100):
    """Get channel action report"""
    items = service.channel_action_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/channel-action/{channel_action_id}")
async def api_channel_action_int_w248_get_channel_action(channel_action_id: str):
    """Get channel action details"""
    item = service.get_channel_action(channel_action_id)
    if not item:
        raise HTTPException(status_code=404, detail="channel_action_int not found")
    return item

@router.post("/api/channel-action/{channel_action_id}/approve")
async def api_channel_action_int_w248_approve_via_channel(channel_action_id: str, request: Request):
    """Approve via channel"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_via_channel(channel_action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="channel_action_int not found")
    return item

@router.post("/api/channel-action/{channel_action_id}/deny")
async def api_channel_action_int_w248_deny_via_channel(channel_action_id: str, request: Request):
    """Deny via channel"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deny_via_channel(channel_action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="channel_action_int not found")
    return item
