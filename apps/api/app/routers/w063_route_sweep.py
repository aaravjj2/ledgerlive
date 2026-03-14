"""Wave 63: Route Sweep E2E Router — E2E route sweep ensuring every route loads, deep refresh works, page root testid present.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w063_route_sweep import service

router = APIRouter(tags=["Route Sweep E2E"])

@router.get("/api/route-sweeps")
async def api_route_sweep_w63_list_sweeps(limit: int = 100):
    """List route sweep results"""
    items = service.list_sweeps(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/route-sweeps", status_code=201)
async def api_route_sweep_w63_run_sweep(request: Request):
    """Run route sweep"""
    data = await request.json()
    item = service.run_sweep(data)
    return item

@router.get("/api/route-sweeps/summary")
async def api_route_sweep_w63_summary(limit: int = 100):
    """Get sweep summary report"""
    items = service.summary(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/route-sweeps/{sweep_id}")
async def api_route_sweep_w63_get_sweep(sweep_id: str):
    """Get sweep result"""
    item = service.get_sweep(sweep_id)
    if not item:
        raise HTTPException(status_code=404, detail="route_sweep not found")
    return item

@router.post("/api/route-sweeps/{sweep_id}/retry")
async def api_route_sweep_w63_retry_failed(sweep_id: str, request: Request):
    """Retry failed routes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.retry_failed(sweep_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="route_sweep not found")
    return item
