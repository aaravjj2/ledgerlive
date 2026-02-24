"""Wave 236: RC Notification Hub v1 Router — Centralized notification hub for Race Control events. Routes notifications by channel (in-app, webhook), applies dedup and throttling, tracks delivery status.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w236_rc_notifications import service

router = APIRouter(tags=["RC Notification Hub v1"])

@router.get("/api/rc-notifications")
async def api_rc_notifications_w236_list_notifications(limit: int = 100):
    """List notifications"""
    items = service.list_notifications(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-notifications", status_code=201)
async def api_rc_notifications_w236_send_notification(request: Request):
    """Send notification"""
    data = await request.json()
    item = service.send_notification(data)
    return item

@router.get("/api/rc-notifications/report")
async def api_rc_notifications_w236_notification_report(limit: int = 100):
    """Get notification hub report"""
    items = service.notification_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-notifications/{notification_id}")
async def api_rc_notifications_w236_get_notification(notification_id: str):
    """Get notification details"""
    item = service.get_notification(notification_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_notifications not found")
    return item

@router.post("/api/rc-notifications/{notification_id}/deliver")
async def api_rc_notifications_w236_mark_delivered(notification_id: str, request: Request):
    """Mark notification delivered"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.mark_delivered(notification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_notifications not found")
    return item

@router.post("/api/rc-notifications/{notification_id}/retry")
async def api_rc_notifications_w236_retry_notification(notification_id: str, request: Request):
    """Retry failed notification"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.retry_notification(notification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_notifications not found")
    return item
