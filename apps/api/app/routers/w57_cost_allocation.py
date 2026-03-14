"""Wave 57: Cost Allocation Router — Cost centers, driver-based allocations, audit chain.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w57_cost_allocation import service

router = APIRouter(tags=["Cost Allocation"])

@router.get("/api/cost-allocations")
async def api_cost_allocation_w57_list_allocations(limit: int = 100):
    """List cost allocations"""
    items = service.list_allocations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/cost-allocations", status_code=201)
async def api_cost_allocation_w57_create_allocation(request: Request):
    """Create a cost allocation"""
    data = await request.json()
    item = service.create_allocation(data)
    return item

@router.get("/api/cost-allocations/drilldown")
async def api_cost_allocation_w57_drilldown(limit: int = 100):
    """Cost allocation drilldown"""
    items = service.drilldown(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cost-allocations/export")
async def api_cost_allocation_w57_export_allocations(limit: int = 100):
    """Export allocations report"""
    items = service.export_allocations(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cost-allocations/{allocation_id}")
async def api_cost_allocation_w57_get_allocation(allocation_id: str):
    """Get allocation details"""
    item = service.get_allocation(allocation_id)
    if not item:
        raise HTTPException(status_code=404, detail="cost_allocation not found")
    return item

@router.post("/api/cost-allocations/{allocation_id}/recalculate")
async def api_cost_allocation_w57_recalculate(allocation_id: str, request: Request):
    """Recalculate allocation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recalculate(allocation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cost_allocation not found")
    return item
