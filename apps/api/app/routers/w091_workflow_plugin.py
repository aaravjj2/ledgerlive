"""Wave 91: Workflow Node Plugins Router — Signed versioned workflow node plugin interface.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w091_workflow_plugin import service

router = APIRouter(tags=["Workflow Node Plugins"])

@router.get("/api/workflow-plugins")
async def api_workflow_plugin_w91_list_plugins(limit: int = 100):
    """List workflow plugins"""
    items = service.list_plugins(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/workflow-plugins", status_code=201)
async def api_workflow_plugin_w91_register_plugin(request: Request):
    """Register a workflow plugin"""
    data = await request.json()
    item = service.register_plugin(data)
    return item

@router.get("/api/workflow-plugins/registry")
async def api_workflow_plugin_w91_plugin_registry(limit: int = 100):
    """Get plugin registry"""
    items = service.plugin_registry(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/workflow-plugins/{plugin_id}")
async def api_workflow_plugin_w91_get_plugin(plugin_id: str):
    """Get plugin details"""
    item = service.get_plugin(plugin_id)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_plugin not found")
    return item

@router.post("/api/workflow-plugins/{plugin_id}/disable")
async def api_workflow_plugin_w91_disable(plugin_id: str, request: Request):
    """Disable plugin"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.disable(plugin_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_plugin not found")
    return item

@router.post("/api/workflow-plugins/{plugin_id}/enable")
async def api_workflow_plugin_w91_enable(plugin_id: str, request: Request):
    """Enable plugin"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.enable(plugin_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_plugin not found")
    return item

@router.post("/api/workflow-plugins/{plugin_id}/verify")
async def api_workflow_plugin_w91_verify_signature(plugin_id: str, request: Request):
    """Verify plugin signature"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_signature(plugin_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_plugin not found")
    return item
