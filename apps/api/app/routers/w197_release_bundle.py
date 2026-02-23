"""Wave 197: Release Bundle v3 Router — Release bundle includes proof pack pointer, deploy smoke reports, environment provenance. Deterministic bundle generation in DEMO mode.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w197_release_bundle import service

router = APIRouter(tags=["Release Bundle v3"])

@router.get("/api/release-bundles")
async def api_release_bundle_w197_list_bundles(limit: int = 100):
    """List release bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/release-bundles", status_code=201)
async def api_release_bundle_w197_generate_bundle(request: Request):
    """Generate release bundle"""
    data = await request.json()
    item = service.generate_bundle(data)
    return item

@router.get("/api/release-bundles/report")
async def api_release_bundle_w197_bundle_report(limit: int = 100):
    """Get release bundle report"""
    items = service.bundle_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/release-bundles/{bundle_id}")
async def api_release_bundle_w197_get_bundle(bundle_id: str):
    """Get bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle not found")
    return item

@router.post("/api/release-bundles/{bundle_id}/determinism")
async def api_release_bundle_w197_verify_determinism(bundle_id: str, request: Request):
    """Verify twice-run hash match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle not found")
    return item

@router.post("/api/release-bundles/{bundle_id}/validate")
async def api_release_bundle_w197_validate_bundle(bundle_id: str, request: Request):
    """Validate bundle completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle not found")
    return item
