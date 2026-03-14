"""Wave 102: ISO Mapping 2.0 Router — ISO control mapping with coverage metrics dashboard.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w102_iso_mapping import service

router = APIRouter(tags=["ISO Mapping 2.0"])

@router.get("/api/iso-mappings")
async def api_iso_mapping_w102_list_mappings(limit: int = 100):
    """List ISO mappings"""
    items = service.list_mappings(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/iso-mappings", status_code=201)
async def api_iso_mapping_w102_create_mapping(request: Request):
    """Create ISO mapping"""
    data = await request.json()
    item = service.create_mapping(data)
    return item

@router.get("/api/iso-mappings/dashboard")
async def api_iso_mapping_w102_coverage_dashboard(limit: int = 100):
    """Get ISO coverage dashboard"""
    items = service.coverage_dashboard(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/iso-mappings/gaps")
async def api_iso_mapping_w102_gap_report(limit: int = 100):
    """Get gap analysis report"""
    items = service.gap_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/iso-mappings/{mapping_id}")
async def api_iso_mapping_w102_get_mapping(mapping_id: str):
    """Get mapping details"""
    item = service.get_mapping(mapping_id)
    if not item:
        raise HTTPException(status_code=404, detail="iso_mapping not found")
    return item

@router.post("/api/iso-mappings/{mapping_id}/assess")
async def api_iso_mapping_w102_assess_coverage(mapping_id: str, request: Request):
    """Assess coverage"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assess_coverage(mapping_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="iso_mapping not found")
    return item
