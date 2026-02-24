"""Wave 257: Tamper Simulation v1 Router — DEMO-only mode that injects controlled integrity failures. UI explains detection and recovery process with deterministic outcomes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w257_tamper_simulation import service

router = APIRouter(tags=["Tamper Simulation v1"])

@router.get("/api/tamper-simulation")
async def api_tamper_simulation_w257_list_simulations(limit: int = 100):
    """List tamper simulations"""
    items = service.list_simulations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tamper-simulation", status_code=201)
async def api_tamper_simulation_w257_run_simulation(request: Request):
    """Run tamper simulation"""
    data = await request.json()
    item = service.run_simulation(data)
    return item

@router.get("/api/tamper-simulation/report")
async def api_tamper_simulation_w257_simulation_report(limit: int = 100):
    """Get tamper simulation report"""
    items = service.simulation_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/tamper-simulation/{simulation_id}")
async def api_tamper_simulation_w257_get_simulation(simulation_id: str):
    """Get simulation details"""
    item = service.get_simulation(simulation_id)
    if not item:
        raise HTTPException(status_code=404, detail="tamper_simulation not found")
    return item

@router.post("/api/tamper-simulation/{simulation_id}/detect")
async def api_tamper_simulation_w257_detect_tamper(simulation_id: str, request: Request):
    """Detect tamper"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.detect_tamper(simulation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tamper_simulation not found")
    return item

@router.post("/api/tamper-simulation/{simulation_id}/inject")
async def api_tamper_simulation_w257_inject_failure(simulation_id: str, request: Request):
    """Inject controlled failure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.inject_failure(simulation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tamper_simulation not found")
    return item

@router.post("/api/tamper-simulation/{simulation_id}/recover")
async def api_tamper_simulation_w257_recover(simulation_id: str, request: Request):
    """Execute recovery"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recover(simulation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tamper_simulation not found")
    return item
