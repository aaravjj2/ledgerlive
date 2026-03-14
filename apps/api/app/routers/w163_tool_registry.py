"""Wave 163: Tool Registry v1 Router — Typed versioned audited tool registry with JSON schemas, strict validation, and tool_trace recording.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w163_tool_registry import service

router = APIRouter(tags=["Tool Registry v1"])

@router.get("/api/tool-registry")
async def api_tool_registry_w163_list_tools(limit: int = 100):
    """List registered tools"""
    items = service.list_tools(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tool-registry", status_code=201)
async def api_tool_registry_w163_register_tool(request: Request):
    """Register a tool with schema"""
    data = await request.json()
    item = service.register_tool(data)
    return item

@router.get("/api/tool-registry/export")
async def api_tool_registry_w163_tool_registry_export(limit: int = 100):
    """Export tool registry"""
    items = service.tool_registry_export(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/tool-registry/{tool_id}")
async def api_tool_registry_w163_get_tool(tool_id: str):
    """Get tool details"""
    item = service.get_tool(tool_id)
    if not item:
        raise HTTPException(status_code=404, detail="tool_registry not found")
    return item

@router.post("/api/tool-registry/{tool_id}/invoke")
async def api_tool_registry_w163_invoke_tool(tool_id: str, request: Request):
    """Invoke tool with args"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.invoke_tool(tool_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tool_registry not found")
    return item

@router.get("/api/tool-registry/{tool_id}/trace")
async def api_tool_registry_w163_get_trace(tool_id: str):
    """Get tool trace history"""
    item = service.get_trace(tool_id)
    if not item:
        raise HTTPException(status_code=404, detail="tool_registry not found")
    return item

@router.post("/api/tool-registry/{tool_id}/validate")
async def api_tool_registry_w163_validate_schema(tool_id: str, request: Request):
    """Validate tool schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_schema(tool_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tool_registry not found")
    return item
