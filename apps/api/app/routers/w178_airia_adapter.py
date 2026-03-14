"""Wave 178: Airia Adapter Skeleton Router — Exporter producing Airia community package artifact: tool schema, runbooks, persona config, screenshots list, metadata. Not published yet.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w178_airia_adapter import service

router = APIRouter(tags=["Airia Adapter Skeleton"])

@router.get("/api/airia-adapter")
async def api_airia_adapter_w178_list_packages(limit: int = 100):
    """List Airia packages"""
    items = service.list_packages(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/airia-adapter", status_code=201)
async def api_airia_adapter_w178_generate_package(request: Request):
    """Generate Airia community package"""
    data = await request.json()
    item = service.generate_package(data)
    return item

@router.get("/api/airia-adapter/report")
async def api_airia_adapter_w178_package_report(limit: int = 100):
    """Get package report"""
    items = service.package_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/airia-adapter/{package_id}")
async def api_airia_adapter_w178_get_package(package_id: str):
    """Get package details"""
    item = service.get_package(package_id)
    if not item:
        raise HTTPException(status_code=404, detail="airia_adapter not found")
    return item

@router.post("/api/airia-adapter/{package_id}/export")
async def api_airia_adapter_w178_export_package(package_id: str, request: Request):
    """Export package artifact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_package(package_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_adapter not found")
    return item

@router.post("/api/airia-adapter/{package_id}/validate")
async def api_airia_adapter_w178_validate_package(package_id: str, request: Request):
    """Validate package"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_package(package_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_adapter not found")
    return item
