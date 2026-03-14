"""Wave 272: Chat Workspace v2 Router — Mock chat workspace with interactive cards, escalation pings, and watcher notifications. Deterministic message ordering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w272_chat_workspace_v2 import service

router = APIRouter(tags=["Chat Workspace v2"])

@router.get("/api/chat-workspace-v2")
async def api_chat_workspace_v2_w272_list_messages(limit: int = 100):
    """List chat messages"""
    items = service.list_messages(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/chat-workspace-v2", status_code=201)
async def api_chat_workspace_v2_w272_send_message(request: Request):
    """Send chat message"""
    data = await request.json()
    item = service.send_message(data)
    return item

@router.get("/api/chat-workspace-v2/report")
async def api_chat_workspace_v2_w272_chat_report(limit: int = 100):
    """Get chat workspace report"""
    items = service.chat_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/chat-workspace-v2/{message_id}")
async def api_chat_workspace_v2_w272_get_message(message_id: str):
    """Get message details"""
    item = service.get_message(message_id)
    if not item:
        raise HTTPException(status_code=404, detail="chat_workspace_v2 not found")
    return item

@router.post("/api/chat-workspace-v2/{message_id}/card")
async def api_chat_workspace_v2_w272_send_card(message_id: str, request: Request):
    """Send interactive card"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.send_card(message_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chat_workspace_v2 not found")
    return item

@router.post("/api/chat-workspace-v2/{message_id}/escalate")
async def api_chat_workspace_v2_w272_escalate(message_id: str, request: Request):
    """Escalate via ping"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.escalate(message_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chat_workspace_v2 not found")
    return item

@router.post("/api/chat-workspace-v2/{message_id}/watcher")
async def api_chat_workspace_v2_w272_add_watcher(message_id: str, request: Request):
    """Add watcher notification"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_watcher(message_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chat_workspace_v2 not found")
    return item
