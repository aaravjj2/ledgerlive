"""Wave 110: Compliance Tour Router — Proof pack: compliance tour and verification tooling.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w110_compliance_tour import service

router = APIRouter(tags=["Compliance Tour"])

@router.get("/api/compliance-tours")
async def api_compliance_tour_w110_list_tours(limit: int = 100):
    """List compliance tours"""
    items = service.list_tours(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/compliance-tours", status_code=201)
async def api_compliance_tour_w110_create_tour(request: Request):
    """Create compliance tour"""
    data = await request.json()
    item = service.create_tour(data)
    return item

@router.get("/api/compliance-tours/export")
async def api_compliance_tour_w110_export_tour(limit: int = 100):
    """Export compliance tour pack"""
    items = service.export_tour(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/compliance-tours/{tour_id}")
async def api_compliance_tour_w110_get_tour(tour_id: str):
    """Get tour details"""
    item = service.get_tour(tour_id)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_tour not found")
    return item

@router.post("/api/compliance-tours/{tour_id}/run")
async def api_compliance_tour_w110_run_tour(tour_id: str, request: Request):
    """Run compliance tour"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_tour(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_tour not found")
    return item

@router.post("/api/compliance-tours/{tour_id}/verify")
async def api_compliance_tour_w110_verify_tour(tour_id: str, request: Request):
    """Verify tour results"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_tour(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_tour not found")
    return item
