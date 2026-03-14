"""Wave 166: Agent Console UI Router — Ops-grade agent console: transcript stream, tool trace stream, verifier results, approvals inbox, run status, export links.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w166_agent_console import service

router = APIRouter(tags=["Agent Console UI"])

@router.get("/api/agent-console")
async def api_agent_console_w166_list_consoles(limit: int = 100):
    """List agent console states"""
    items = service.list_consoles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/agent-console", status_code=201)
async def api_agent_console_w166_create_console(request: Request):
    """Create agent console session"""
    data = await request.json()
    item = service.create_console(data)
    return item

@router.get("/api/agent-console/report")
async def api_agent_console_w166_console_report(limit: int = 100):
    """Get console report"""
    items = service.console_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/agent-console/{console_id}")
async def api_agent_console_w166_get_console(console_id: str):
    """Get console state"""
    item = service.get_console(console_id)
    if not item:
        raise HTTPException(status_code=404, detail="agent_console not found")
    return item

@router.post("/api/agent-console/{console_id}/approve")
async def api_agent_console_w166_approve_item(console_id: str, request: Request):
    """Approve item from console"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_item(console_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_console not found")
    return item

@router.post("/api/agent-console/{console_id}/export")
async def api_agent_console_w166_export_from_console(console_id: str, request: Request):
    """Export from console"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_from_console(console_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_console not found")
    return item

@router.post("/api/agent-console/{console_id}/refresh")
async def api_agent_console_w166_refresh_console(console_id: str, request: Request):
    """Refresh console data"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.refresh_console(console_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_console not found")
    return item
