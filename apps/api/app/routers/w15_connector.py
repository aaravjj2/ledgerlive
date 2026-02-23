"""Wave 15: External Connector Router — Connectors for ERP, bank, and payment system integration.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w15_connector import service

router = APIRouter(tags=["External Connector"])

@router.get("/api/connectors")
async def api_list(limit: int = 100):
    """List connectors"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/connectors", status_code=201)
async def api_create(request: Request):
    """Create a connector"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/connectors/{connector_id}")
async def api_get(connector_id: str):
    """Get connector details"""
    item = service.get(connector_id)
    if not item:
        raise HTTPException(status_code=404, detail="connector not found")
    return item

@router.post("/api/connectors/{connector_id}/sync")
async def api_sync(connector_id: str, request: Request):
    """Trigger sync"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sync(connector_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector not found")
    return item

@router.post("/api/connectors/{connector_id}/test")
async def api_test_conn(connector_id: str, request: Request):
    """Test connector"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_conn(connector_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector not found")
    return item
