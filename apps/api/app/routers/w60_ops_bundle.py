"""Wave 60: Enterprise Ops Bundle Router — One-click ops evidence export: job runs, alerts, quality scores, lineage, proof index.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w60_ops_bundle import service

router = APIRouter(tags=["Enterprise Ops Bundle"])

@router.get("/api/ops-bundles")
async def api_ops_bundle_w60_list_bundles(limit: int = 100):
    """List ops bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ops-bundles", status_code=201)
async def api_ops_bundle_w60_create_bundle(request: Request):
    """Create an ops bundle"""
    data = await request.json()
    item = service.create_bundle(data)
    return item

@router.get("/api/ops-bundles/export")
async def api_ops_bundle_w60_export_bundle(limit: int = 100):
    """Export ops bundle"""
    items = service.export_bundle(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ops-bundles/{bundle_id}")
async def api_ops_bundle_w60_get_bundle(bundle_id: str):
    """Get ops bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="ops_bundle not found")
    return item

@router.post("/api/ops-bundles/{bundle_id}/evidence")
async def api_ops_bundle_w60_add_evidence(bundle_id: str, request: Request):
    """Add evidence to bundle"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_evidence(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ops_bundle not found")
    return item

@router.post("/api/ops-bundles/{bundle_id}/hash")
async def api_ops_bundle_w60_compute_hash(bundle_id: str, request: Request):
    """Compute bundle content hash"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compute_hash(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ops_bundle not found")
    return item

@router.post("/api/ops-bundles/{bundle_id}/verify")
async def api_ops_bundle_w60_verify_bundle(bundle_id: str, request: Request):
    """Verify bundle integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ops_bundle not found")
    return item
