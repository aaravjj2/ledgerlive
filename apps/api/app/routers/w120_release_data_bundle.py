"""Wave 120: Release Data Bundle Router — Release bundle including full data platform evidence.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w120_release_data_bundle import service

router = APIRouter(tags=["Release Data Bundle"])

@router.get("/api/release-data-bundles")
async def api_release_data_bundle_w120_list_bundles(limit: int = 100):
    """List release data bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/release-data-bundles", status_code=201)
async def api_release_data_bundle_w120_create_bundle(request: Request):
    """Create release data bundle"""
    data = await request.json()
    item = service.create_bundle(data)
    return item

@router.get("/api/release-data-bundles/export")
async def api_release_data_bundle_w120_export_bundle(limit: int = 100):
    """Export release data bundle"""
    items = service.export_bundle(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/release-data-bundles/{bundle_id}")
async def api_release_data_bundle_w120_get_bundle(bundle_id: str):
    """Get bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_data_bundle not found")
    return item

@router.post("/api/release-data-bundles/{bundle_id}/verify")
async def api_release_data_bundle_w120_verify_bundle(bundle_id: str, request: Request):
    """Verify bundle integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_data_bundle not found")
    return item
