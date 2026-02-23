"""Wave 23: Compliance Bundle Router — Assemble compliance evidence bundles for regulatory filings.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w23_compliance_bundle import service

router = APIRouter(tags=["Compliance Bundle"])

@router.get("/api/compliance-bundles")
async def api_list(limit: int = 100):
    """List compliance bundles"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/compliance-bundles", status_code=201)
async def api_create(request: Request):
    """Create a compliance bundle"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/compliance-bundles/{bundle_id}")
async def api_get(bundle_id: str):
    """Get bundle details"""
    item = service.get(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_bundle not found")
    return item

@router.post("/api/compliance-bundles/{bundle_id}/items")
async def api_add_item(bundle_id: str, request: Request):
    """Add item to bundle"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_item(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_bundle not found")
    return item

@router.post("/api/compliance-bundles/{bundle_id}/submit")
async def api_submit(bundle_id: str, request: Request):
    """Submit for review"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.submit(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_bundle not found")
    return item
