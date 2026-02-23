"""Wave 43: Xero Connector Router — Xero sync with same contract guarantees as QBO. Mapping and idempotent sync.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w43_xero_connector import service

router = APIRouter(tags=["Xero Connector"])

@router.get("/api/xero/mock-contract")
async def api_xero_connector_w43_mock_contract(limit: int = 100):
    """Get Xero mock contract spec"""
    items = service.mock_contract(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/xero/syncs")
async def api_xero_connector_w43_list_syncs(limit: int = 100):
    """List Xero sync runs"""
    items = service.list_syncs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/xero/syncs", status_code=201)
async def api_xero_connector_w43_start_sync(request: Request):
    """Start a Xero sync"""
    data = await request.json()
    item = service.start_sync(data)
    return item

@router.get("/api/xero/syncs/{sync_id}")
async def api_xero_connector_w43_get_sync(sync_id: str):
    """Get Xero sync details"""
    item = service.get_sync(sync_id)
    if not item:
        raise HTTPException(status_code=404, detail="xero_connector not found")
    return item

@router.post("/api/xero/syncs/{sync_id}/cancel")
async def api_xero_connector_w43_cancel_sync(sync_id: str, request: Request):
    """Cancel a running sync"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.cancel_sync(sync_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="xero_connector not found")
    return item

@router.post("/api/xero/syncs/{sync_id}/retry")
async def api_xero_connector_w43_retry_sync(sync_id: str, request: Request):
    """Retry failed sync"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.retry_sync(sync_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="xero_connector not found")
    return item
