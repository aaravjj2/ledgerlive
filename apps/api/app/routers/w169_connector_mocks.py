"""Wave 169: Connector Mock Servers v1 Router — Local mock servers for QBO/Xero/Plaid simulating pagination, token refresh, 429 backoff, partial responses, dirty data.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w169_connector_mocks import service

router = APIRouter(tags=["Connector Mock Servers v1"])

@router.get("/api/connector-mocks")
async def api_connector_mocks_w169_list_mocks(limit: int = 100):
    """List mock server configs"""
    items = service.list_mocks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/connector-mocks", status_code=201)
async def api_connector_mocks_w169_create_mock(request: Request):
    """Create mock server config"""
    data = await request.json()
    item = service.create_mock(data)
    return item

@router.get("/api/connector-mocks/report")
async def api_connector_mocks_w169_mock_report(limit: int = 100):
    """Get mock sync report"""
    items = service.mock_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/connector-mocks/status")
async def api_connector_mocks_w169_mock_status(limit: int = 100):
    """Get mock server status"""
    items = service.mock_status(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/connector-mocks/{mock_id}")
async def api_connector_mocks_w169_get_mock(mock_id: str):
    """Get mock config details"""
    item = service.get_mock(mock_id)
    if not item:
        raise HTTPException(status_code=404, detail="connector_mocks not found")
    return item

@router.post("/api/connector-mocks/{mock_id}/sync")
async def api_connector_mocks_w169_sync_mock(mock_id: str, request: Request):
    """Sync data from mock"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sync_mock(mock_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_mocks not found")
    return item

@router.post("/api/connector-mocks/{mock_id}/toggle-error")
async def api_connector_mocks_w169_toggle_error(mock_id: str, request: Request):
    """Toggle error simulation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.toggle_error(mock_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_mocks not found")
    return item
