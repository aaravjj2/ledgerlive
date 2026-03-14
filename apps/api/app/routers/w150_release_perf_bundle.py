"""Wave 150: Release Performance Bundle Router — Release bundle including full performance evidence.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w150_release_perf_bundle import service

router = APIRouter(tags=["Release Performance Bundle"])

@router.get("/api/release-perf-bundles")
async def api_release_perf_bundle_w150_list_bundles(limit: int = 100):
    """List release perf bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/release-perf-bundles", status_code=201)
async def api_release_perf_bundle_w150_create_bundle(request: Request):
    """Create release perf bundle"""
    data = await request.json()
    item = service.create_bundle(data)
    return item

@router.get("/api/release-perf-bundles/export")
async def api_release_perf_bundle_w150_export_bundle(limit: int = 100):
    """Export release perf bundle"""
    items = service.export_bundle(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/release-perf-bundles/{bundle_id}")
async def api_release_perf_bundle_w150_get_bundle(bundle_id: str):
    """Get bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_perf_bundle not found")
    return item

@router.post("/api/release-perf-bundles/{bundle_id}/verify")
async def api_release_perf_bundle_w150_verify_bundle(bundle_id: str, request: Request):
    """Verify bundle"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_perf_bundle not found")
    return item
