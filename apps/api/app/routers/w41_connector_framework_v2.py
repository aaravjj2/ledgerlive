"""Wave 41: Connector Framework 2.0 Router — Connector capability model with scopes, UI connection manager, sync scheduling.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w41_connector_framework_v2 import service

router = APIRouter(tags=["Connector Framework 2.0"])

@router.get("/api/connectors-v2")
async def api_connector_framework_v2_w41_list_connectors(limit: int = 100):
    """List connectors v2"""
    items = service.list_connectors(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/connectors-v2", status_code=201)
async def api_connector_framework_v2_w41_register(request: Request):
    """Register a connector"""
    data = await request.json()
    item = service.register(data)
    return item

@router.get("/api/connectors-v2/history")
async def api_connector_framework_v2_w41_sync_history(limit: int = 100):
    """Get sync history"""
    items = service.sync_history(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/connectors-v2/{connector_id}")
async def api_connector_framework_v2_w41_get_connector(connector_id: str):
    """Get connector details"""
    item = service.get_connector(connector_id)
    if not item:
        raise HTTPException(status_code=404, detail="connector_framework_v2 not found")
    return item

@router.post("/api/connectors-v2/{connector_id}/configure")
async def api_connector_framework_v2_w41_configure(connector_id: str, request: Request):
    """Configure connector"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.configure(connector_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_framework_v2 not found")
    return item

@router.post("/api/connectors-v2/{connector_id}/sync")
async def api_connector_framework_v2_w41_sync_now(connector_id: str, request: Request):
    """Trigger sync"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sync_now(connector_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_framework_v2 not found")
    return item

@router.post("/api/connectors-v2/{connector_id}/test")
async def api_connector_framework_v2_w41_test_connection(connector_id: str, request: Request):
    """Test connector connection"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_connection(connector_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_framework_v2 not found")
    return item
