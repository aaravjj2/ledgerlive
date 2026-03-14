"""Wave 184: Airia Package Finalizer v1 Router — Publish-ready Airia community bundle: tool schema, runbooks, persona config, metadata, deterministic file ordering, checksums. Strict validator.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w184_airia_finalizer import service

router = APIRouter(tags=["Airia Package Finalizer v1"])

@router.get("/api/airia-finalizer")
async def api_airia_finalizer_w184_list_bundles(limit: int = 100):
    """List Airia bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/airia-finalizer", status_code=201)
async def api_airia_finalizer_w184_generate_bundle(request: Request):
    """Generate publish-ready Airia bundle"""
    data = await request.json()
    item = service.generate_bundle(data)
    return item

@router.get("/api/airia-finalizer/report")
async def api_airia_finalizer_w184_bundle_report(limit: int = 100):
    """Get bundle generation report"""
    items = service.bundle_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/airia-finalizer/{bundle_id}")
async def api_airia_finalizer_w184_get_bundle(bundle_id: str):
    """Get bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="airia_finalizer not found")
    return item

@router.post("/api/airia-finalizer/{bundle_id}/export")
async def api_airia_finalizer_w184_export_bundle(bundle_id: str, request: Request):
    """Export bundle artifact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_finalizer not found")
    return item

@router.post("/api/airia-finalizer/{bundle_id}/validate")
async def api_airia_finalizer_w184_validate_bundle(bundle_id: str, request: Request):
    """Validate bundle completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_finalizer not found")
    return item
