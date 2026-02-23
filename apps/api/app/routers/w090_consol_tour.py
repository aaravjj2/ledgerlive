"""Wave 90: Consolidation Tour Router — Proof pack with consolidation tour and determinism verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w090_consol_tour import service

router = APIRouter(tags=["Consolidation Tour"])

@router.get("/api/consol-tours")
async def api_consol_tour_w90_list_tours(limit: int = 100):
    """List consolidation tours"""
    items = service.list_tours(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/consol-tours", status_code=201)
async def api_consol_tour_w90_create_tour(request: Request):
    """Create consolidation tour"""
    data = await request.json()
    item = service.create_tour(data)
    return item

@router.get("/api/consol-tours/export")
async def api_consol_tour_w90_export_tour(limit: int = 100):
    """Export tour proof pack"""
    items = service.export_tour(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/consol-tours/{tour_id}")
async def api_consol_tour_w90_get_tour(tour_id: str):
    """Get tour details"""
    item = service.get_tour(tour_id)
    if not item:
        raise HTTPException(status_code=404, detail="consol_tour not found")
    return item

@router.post("/api/consol-tours/{tour_id}/run")
async def api_consol_tour_w90_run_tour(tour_id: str, request: Request):
    """Run consolidation tour"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_tour(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_tour not found")
    return item

@router.post("/api/consol-tours/{tour_id}/verify")
async def api_consol_tour_w90_verify_determinism(tour_id: str, request: Request):
    """Verify determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(tour_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_tour not found")
    return item
