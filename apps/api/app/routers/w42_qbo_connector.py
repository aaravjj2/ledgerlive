"""Wave 42: QuickBooks Online Connector Router — QBO auth flow scaffolding (flagged), sync invoices, COA, payments. Mock-first.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w42_qbo_connector import service

router = APIRouter(tags=["QuickBooks Online Connector"])

@router.get("/api/qbo/mock-contract")
async def api_qbo_connector_w42_mock_contract(limit: int = 100):
    """Get QBO mock contract spec"""
    items = service.mock_contract(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/qbo/syncs")
async def api_qbo_connector_w42_list_syncs(limit: int = 100):
    """List QBO sync runs"""
    items = service.list_syncs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/qbo/syncs", status_code=201)
async def api_qbo_connector_w42_start_sync(request: Request):
    """Start a QBO sync"""
    data = await request.json()
    item = service.start_sync(data)
    return item

@router.get("/api/qbo/syncs/{sync_id}")
async def api_qbo_connector_w42_get_sync(sync_id: str):
    """Get QBO sync details"""
    item = service.get_sync(sync_id)
    if not item:
        raise HTTPException(status_code=404, detail="qbo_connector not found")
    return item

@router.post("/api/qbo/syncs/{sync_id}/cancel")
async def api_qbo_connector_w42_cancel_sync(sync_id: str, request: Request):
    """Cancel a running sync"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.cancel_sync(sync_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="qbo_connector not found")
    return item

@router.post("/api/qbo/syncs/{sync_id}/retry")
async def api_qbo_connector_w42_retry_sync(sync_id: str, request: Request):
    """Retry failed sync"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.retry_sync(sync_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="qbo_connector not found")
    return item
