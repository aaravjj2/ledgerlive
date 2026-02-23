"""Wave 170: Connector Real-Mode Interface Router — Real provider interfaces behind ENABLE_QBO/ENABLE_XERO/ENABLE_PLAID flags. Keys optional, never required. Fail fast without keys.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w170_connector_realmode import service

router = APIRouter(tags=["Connector Real-Mode Interface"])

@router.get("/api/connector-realmode")
async def api_connector_realmode_w170_list_configs(limit: int = 100):
    """List real-mode configs"""
    items = service.list_configs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/connector-realmode", status_code=201)
async def api_connector_realmode_w170_create_config(request: Request):
    """Create real-mode config"""
    data = await request.json()
    item = service.create_config(data)
    return item

@router.get("/api/connector-realmode/report")
async def api_connector_realmode_w170_config_report(limit: int = 100):
    """Get config validation report"""
    items = service.config_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/connector-realmode/{config_id}")
async def api_connector_realmode_w170_get_config(config_id: str):
    """Get config details"""
    item = service.get_config(config_id)
    if not item:
        raise HTTPException(status_code=404, detail="connector_realmode not found")
    return item

@router.post("/api/connector-realmode/{config_id}/test")
async def api_connector_realmode_w170_test_connection(config_id: str, request: Request):
    """Test connection safely"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_connection(config_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_realmode not found")
    return item

@router.post("/api/connector-realmode/{config_id}/validate")
async def api_connector_realmode_w170_validate_keys(config_id: str, request: Request):
    """Validate provider keys"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_keys(config_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_realmode not found")
    return item
