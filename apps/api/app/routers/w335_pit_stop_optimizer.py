"""Wave 335: Pit Stop Optimizer v1 Router — Suggests next-best step ordering given blockers (deterministic).

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w335_pit_stop_optimizer import service

router = APIRouter(tags=["Pit Stop Optimizer v1"])

@router.get("/api/pit-stop-optimizer")
async def api_pit_stop_optimizer_w335_list_optimizations(limit: int = 100):
    """List optimizations"""
    items = service.list_optimizations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/pit-stop-optimizer", status_code=201)
async def api_pit_stop_optimizer_w335_optimize(request: Request):
    """Run pit stop optimization"""
    data = await request.json()
    item = service.optimize(data)
    return item

@router.get("/api/pit-stop-optimizer/report")
async def api_pit_stop_optimizer_w335_optimizer_report(limit: int = 100):
    """Get optimizer report"""
    items = service.optimizer_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/pit-stop-optimizer/{optimizer_id}")
async def api_pit_stop_optimizer_w335_get_optimization(optimizer_id: str):
    """Get optimization details"""
    item = service.get_optimization(optimizer_id)
    if not item:
        raise HTTPException(status_code=404, detail="pit_stop_optimizer not found")
    return item

@router.post("/api/pit-stop-optimizer/{optimizer_id}/apply")
async def api_pit_stop_optimizer_w335_apply_suggestion(optimizer_id: str, request: Request):
    """Apply suggested order"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_suggestion(optimizer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="pit_stop_optimizer not found")
    return item

@router.post("/api/pit-stop-optimizer/{optimizer_id}/reoptimize")
async def api_pit_stop_optimizer_w335_reoptimize(optimizer_id: str, request: Request):
    """Reoptimize with new data"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reoptimize(optimizer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="pit_stop_optimizer not found")
    return item
