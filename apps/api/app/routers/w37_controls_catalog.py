"""Wave 37: Controls Catalog Router — SOX-style controls mapped to workflows and required evidence artifacts.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w37_controls_catalog import service

router = APIRouter(tags=["Controls Catalog"])

@router.get("/api/controls")
async def api_controls_catalog_w37_list_controls(limit: int = 100):
    """List controls"""
    items = service.list_controls(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/controls", status_code=201)
async def api_controls_catalog_w37_create_control(request: Request):
    """Create a control"""
    data = await request.json()
    item = service.create_control(data)
    return item

@router.get("/api/controls/coverage")
async def api_controls_catalog_w37_export_coverage(limit: int = 100):
    """Export controls coverage report"""
    items = service.export_coverage(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/controls/{control_id}")
async def api_controls_catalog_w37_get_control(control_id: str):
    """Get control details"""
    item = service.get_control(control_id)
    if not item:
        raise HTTPException(status_code=404, detail="controls_catalog not found")
    return item

@router.post("/api/controls/{control_id}/evidence")
async def api_controls_catalog_w37_map_evidence(control_id: str, request: Request):
    """Map evidence to control"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.map_evidence(control_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="controls_catalog not found")
    return item

@router.post("/api/controls/{control_id}/test")
async def api_controls_catalog_w37_test_control(control_id: str, request: Request):
    """Test/verify a control"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_control(control_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="controls_catalog not found")
    return item
