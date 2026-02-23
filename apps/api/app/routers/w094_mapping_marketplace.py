"""Wave 94: Mapping Template Marketplace Router — COA/vendor/tax mapping signed templates for import/export.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w094_mapping_marketplace import service

router = APIRouter(tags=["Mapping Template Marketplace"])

@router.get("/api/mapping-marketplace")
async def api_mapping_marketplace_w94_list_mappings(limit: int = 100):
    """List mapping templates"""
    items = service.list_mappings(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/mapping-marketplace", status_code=201)
async def api_mapping_marketplace_w94_publish(request: Request):
    """Publish mapping template"""
    data = await request.json()
    item = service.publish(data)
    return item

@router.get("/api/mapping-marketplace/export")
async def api_mapping_marketplace_w94_export_mappings(limit: int = 100):
    """Export mappings bundle"""
    items = service.export_mappings(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/mapping-marketplace/{mapping_id}")
async def api_mapping_marketplace_w94_get_mapping(mapping_id: str):
    """Get mapping details"""
    item = service.get_mapping(mapping_id)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_marketplace not found")
    return item

@router.post("/api/mapping-marketplace/{mapping_id}/import")
async def api_mapping_marketplace_w94_import_mapping(mapping_id: str, request: Request):
    """Import mapping"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.import_mapping(mapping_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_marketplace not found")
    return item

@router.post("/api/mapping-marketplace/{mapping_id}/verify")
async def api_mapping_marketplace_w94_verify_mapping(mapping_id: str, request: Request):
    """Verify mapping signature"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_mapping(mapping_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_marketplace not found")
    return item
