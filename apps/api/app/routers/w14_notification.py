"""Wave 14: Notification Service Router — Event-driven notifications for close milestones.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w14_notification import service

router = APIRouter(tags=["Notification Service"])

@router.get("/api/notifications")
async def api_list(limit: int = 100):
    """List notifications"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/notifications", status_code=201)
async def api_send(request: Request):
    """Send a notification"""
    data = await request.json()
    item = service.send(data)
    return item

@router.get("/api/notifications/stats")
async def api_stats(limit: int = 100):
    """Notification statistics"""
    items = service.stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/notifications/{notification_id}")
async def api_get(notification_id: str):
    """Get notification details"""
    item = service.get(notification_id)
    if not item:
        raise HTTPException(status_code=404, detail="notification not found")
    return item

@router.post("/api/notifications/{notification_id}/read")
async def api_mark_read(notification_id: str, request: Request):
    """Mark notification read"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.mark_read(notification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="notification not found")
    return item
