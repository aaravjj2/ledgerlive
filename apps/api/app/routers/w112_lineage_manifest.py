"""Wave 112: Lineage Manifest 2.0 Router — Source-hash lineage manifests for every export and run.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w112_lineage_manifest import service

router = APIRouter(tags=["Lineage Manifest 2.0"])

@router.get("/api/lineage-manifests")
async def api_lineage_manifest_w112_list_manifests(limit: int = 100):
    """List lineage manifests"""
    items = service.list_manifests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/lineage-manifests", status_code=201)
async def api_lineage_manifest_w112_create_manifest(request: Request):
    """Create lineage manifest"""
    data = await request.json()
    item = service.create_manifest(data)
    return item

@router.get("/api/lineage-manifests/export")
async def api_lineage_manifest_w112_export_manifest(limit: int = 100):
    """Export lineage manifests"""
    items = service.export_manifest(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/lineage-manifests/tree")
async def api_lineage_manifest_w112_lineage_tree(limit: int = 100):
    """Get full lineage tree"""
    items = service.lineage_tree(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/lineage-manifests/{manifest_id}")
async def api_lineage_manifest_w112_get_manifest(manifest_id: str):
    """Get manifest details"""
    item = service.get_manifest(manifest_id)
    if not item:
        raise HTTPException(status_code=404, detail="lineage_manifest not found")
    return item

@router.post("/api/lineage-manifests/{manifest_id}/verify")
async def api_lineage_manifest_w112_verify_manifest(manifest_id: str, request: Request):
    """Verify manifest integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_manifest(manifest_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="lineage_manifest not found")
    return item
