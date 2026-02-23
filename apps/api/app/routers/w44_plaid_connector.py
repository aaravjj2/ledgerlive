"""Wave 44: Plaid Connector Router — Plaid bank feed scaffolding (flagged), transaction sync, dedupe, enrichment.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w44_plaid_connector import service

router = APIRouter(tags=["Plaid Connector"])

@router.get("/api/plaid/feeds")
async def api_plaid_connector_w44_list_feeds(limit: int = 100):
    """List Plaid bank feeds"""
    items = service.list_feeds(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/plaid/feeds", status_code=201)
async def api_plaid_connector_w44_create_feed(request: Request):
    """Create a bank feed"""
    data = await request.json()
    item = service.create_feed(data)
    return item

@router.get("/api/plaid/mock-contract")
async def api_plaid_connector_w44_mock_contract(limit: int = 100):
    """Get Plaid mock contract spec"""
    items = service.mock_contract(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/plaid/feeds/{feed_id}")
async def api_plaid_connector_w44_get_feed(feed_id: str):
    """Get feed details"""
    item = service.get_feed(feed_id)
    if not item:
        raise HTTPException(status_code=404, detail="plaid_connector not found")
    return item

@router.post("/api/plaid/feeds/{feed_id}/dedupe")
async def api_plaid_connector_w44_dedupe(feed_id: str, request: Request):
    """Run deduplication"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.dedupe(feed_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="plaid_connector not found")
    return item

@router.post("/api/plaid/feeds/{feed_id}/enrich")
async def api_plaid_connector_w44_enrich(feed_id: str, request: Request):
    """Enrich transactions"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.enrich(feed_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="plaid_connector not found")
    return item

@router.post("/api/plaid/feeds/{feed_id}/sync")
async def api_plaid_connector_w44_sync_transactions(feed_id: str, request: Request):
    """Sync transactions"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sync_transactions(feed_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="plaid_connector not found")
    return item
