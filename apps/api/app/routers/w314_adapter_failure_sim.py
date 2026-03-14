"""Wave 314: Adapter Failure Simulation v1 Router — Adapter failures become incidents with deterministic recovery audit trails.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w314_adapter_failure_sim import service

router = APIRouter(tags=["Adapter Failure Simulation v1"])

@router.get("/api/adapter-failure-sim")
async def api_adapter_failure_sim_w314_list_sims(limit: int = 100):
    """List failure simulations"""
    items = service.list_sims(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/adapter-failure-sim", status_code=201)
async def api_adapter_failure_sim_w314_create_sim(request: Request):
    """Create failure simulation"""
    data = await request.json()
    item = service.create_sim(data)
    return item

@router.get("/api/adapter-failure-sim/report")
async def api_adapter_failure_sim_w314_sim_report(limit: int = 100):
    """Get simulation report"""
    items = service.sim_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/adapter-failure-sim/{sim_id}")
async def api_adapter_failure_sim_w314_get_sim(sim_id: str):
    """Get simulation details"""
    item = service.get_sim(sim_id)
    if not item:
        raise HTTPException(status_code=404, detail="adapter_failure_sim not found")
    return item

@router.post("/api/adapter-failure-sim/{sim_id}/inject")
async def api_adapter_failure_sim_w314_inject_failure(sim_id: str, request: Request):
    """Inject adapter failure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.inject_failure(sim_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adapter_failure_sim not found")
    return item

@router.post("/api/adapter-failure-sim/{sim_id}/recover")
async def api_adapter_failure_sim_w314_recover(sim_id: str, request: Request):
    """Attempt recovery"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recover(sim_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adapter_failure_sim not found")
    return item
