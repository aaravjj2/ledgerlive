"""Wave 53: Driver-based Planning Router — Drivers (headcount, units, pricing), propagation engine, cycle detection.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w53_driver_planning import service

router = APIRouter(tags=["Driver-based Planning"])

@router.get("/api/drivers")
async def api_driver_planning_w53_list_drivers(limit: int = 100):
    """List planning drivers"""
    items = service.list_drivers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/drivers", status_code=201)
async def api_driver_planning_w53_create_driver(request: Request):
    """Create a planning driver"""
    data = await request.json()
    item = service.create_driver(data)
    return item

@router.get("/api/drivers/export-graph")
async def api_driver_planning_w53_export_graph(limit: int = 100):
    """Export driver dependency graph"""
    items = service.export_graph(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/drivers/{driver_id}")
async def api_driver_planning_w53_get_driver(driver_id: str):
    """Get driver details"""
    item = service.get_driver(driver_id)
    if not item:
        raise HTTPException(status_code=404, detail="driver_planning not found")
    return item

@router.post("/api/drivers/{driver_id}/check-cycles")
async def api_driver_planning_w53_check_cycles(driver_id: str, request: Request):
    """Check for dependency cycles"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_cycles(driver_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="driver_planning not found")
    return item

@router.post("/api/drivers/{driver_id}/propagate")
async def api_driver_planning_w53_propagate(driver_id: str, request: Request):
    """Propagate driver changes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.propagate(driver_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="driver_planning not found")
    return item

@router.post("/api/drivers/{driver_id}/update-value")
async def api_driver_planning_w53_update_value(driver_id: str, request: Request):
    """Update driver value"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.update_value(driver_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="driver_planning not found")
    return item
