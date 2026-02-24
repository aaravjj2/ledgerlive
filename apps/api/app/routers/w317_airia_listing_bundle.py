"""Wave 317: Airia Listing Bundle v1 Router — Generate agent listing metadata (name, description, tags) and screenshots manifest.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w317_airia_listing_bundle import service

router = APIRouter(tags=["Airia Listing Bundle v1"])

@router.get("/api/airia-listing-bundle")
async def api_airia_listing_bundle_w317_list_bundles(limit: int = 100):
    """List listing bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/airia-listing-bundle", status_code=201)
async def api_airia_listing_bundle_w317_create_bundle(request: Request):
    """Create listing bundle"""
    data = await request.json()
    item = service.create_bundle(data)
    return item

@router.get("/api/airia-listing-bundle/report")
async def api_airia_listing_bundle_w317_bundle_report(limit: int = 100):
    """Get listing bundle report"""
    items = service.bundle_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/airia-listing-bundle/{bundle_id}")
async def api_airia_listing_bundle_w317_get_bundle(bundle_id: str):
    """Get bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="airia_listing_bundle not found")
    return item

@router.post("/api/airia-listing-bundle/{bundle_id}/manifest")
async def api_airia_listing_bundle_w317_generate_manifest(bundle_id: str, request: Request):
    """Generate screenshots manifest"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_manifest(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_listing_bundle not found")
    return item

@router.post("/api/airia-listing-bundle/{bundle_id}/metadata")
async def api_airia_listing_bundle_w317_update_metadata(bundle_id: str, request: Request):
    """Update metadata"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.update_metadata(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_listing_bundle not found")
    return item
