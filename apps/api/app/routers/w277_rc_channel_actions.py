"""Wave 277: RC Channel Actions v1 Router — Send to channel actions for approvals and incidents from Race Control. No network in CI with deterministic routing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w277_rc_channel_actions import service

router = APIRouter(tags=["RC Channel Actions v1"])

@router.get("/api/rc-channel-actions")
async def api_rc_channel_actions_w277_list_rc_actions(limit: int = 100):
    """List RC channel actions"""
    items = service.list_rc_actions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-channel-actions", status_code=201)
async def api_rc_channel_actions_w277_create_rc_action(request: Request):
    """Create RC channel action"""
    data = await request.json()
    item = service.create_rc_action(data)
    return item

@router.get("/api/rc-channel-actions/report")
async def api_rc_channel_actions_w277_rc_action_report(limit: int = 100):
    """Get RC channel actions report"""
    items = service.rc_action_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-channel-actions/{rc_action_id}")
async def api_rc_channel_actions_w277_get_rc_action(rc_action_id: str):
    """Get RC action details"""
    item = service.get_rc_action(rc_action_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_channel_actions not found")
    return item

@router.post("/api/rc-channel-actions/{rc_action_id}/confirm")
async def api_rc_channel_actions_w277_confirm_delivery(rc_action_id: str, request: Request):
    """Confirm delivery"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.confirm_delivery(rc_action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_channel_actions not found")
    return item

@router.post("/api/rc-channel-actions/{rc_action_id}/route")
async def api_rc_channel_actions_w277_route_to_channel(rc_action_id: str, request: Request):
    """Route to channel"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.route_to_channel(rc_action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_channel_actions not found")
    return item
