"""Wave 69: Tour Spec Manager Router — TOUR spec covering all core flows >=240s with 20+ named checkpoints.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w069_tour_spec import service

router = APIRouter(tags=["Tour Spec Manager"])

@router.get("/api/tour-specs")
async def api_tour_spec_w69_list_tours(limit: int = 100):
    """List tour specs"""
    items = service.list_tours(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tour-specs", status_code=201)
async def api_tour_spec_w69_create_tour(request: Request):
    """Create a tour spec"""
    data = await request.json()
    item = service.create_tour(data)
    return item

@router.get("/api/tour-specs/export")
async def api_tour_spec_w69_export_tour(limit: int = 100):
    """Export tour bundle"""
    items = service.export_tour(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/tour-specs/{tour_id}")
async def api_tour_spec_w69_get_tour(tour_id: str):
    """Get tour spec details"""
    item = service.get_tour(tour_id)
    if not item:
        raise HTTPException(status_code=404, detail="tour_spec not found")
    return item

@router.post("/api/tour-specs/{tour_id}/checkpoint")
async def api_tour_spec_w69_add_checkpoint(tour_id: str, request: Request):
    """Add named checkpoint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_checkpoint(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tour_spec not found")
    return item

@router.post("/api/tour-specs/{tour_id}/run")
async def api_tour_spec_w69_run_tour(tour_id: str, request: Request):
    """Execute tour recording"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_tour(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tour_spec not found")
    return item

@router.post("/api/tour-specs/{tour_id}/verify")
async def api_tour_spec_w69_verify_tour(tour_id: str, request: Request):
    """Verify tour completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_tour(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tour_spec not found")
    return item
