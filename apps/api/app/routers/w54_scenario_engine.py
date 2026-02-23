"""Wave 54: Scenario Engine Router — Seeded Monte Carlo scenarios, tail risk summary, deterministic outputs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w54_scenario_engine import service

router = APIRouter(tags=["Scenario Engine"])

@router.get("/api/scenarios")
async def api_scenario_engine_w54_list_scenarios(limit: int = 100):
    """List scenarios"""
    items = service.list_scenarios(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/scenarios", status_code=201)
async def api_scenario_engine_w54_create_scenario(request: Request):
    """Create a scenario run"""
    data = await request.json()
    item = service.create_scenario(data)
    return item

@router.get("/api/scenarios/compare")
async def api_scenario_engine_w54_compare_scenarios(limit: int = 100):
    """Compare scenario outcomes"""
    items = service.compare_scenarios(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/scenarios/tail-risk")
async def api_scenario_engine_w54_tail_risk(limit: int = 100):
    """Get tail risk summary"""
    items = service.tail_risk(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/scenarios/{scenario_id}")
async def api_scenario_engine_w54_get_scenario(scenario_id: str):
    """Get scenario details"""
    item = service.get_scenario(scenario_id)
    if not item:
        raise HTTPException(status_code=404, detail="scenario_engine not found")
    return item

@router.post("/api/scenarios/{scenario_id}/simulate")
async def api_scenario_engine_w54_run_simulation(scenario_id: str, request: Request):
    """Run Monte Carlo simulation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_simulation(scenario_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="scenario_engine not found")
    return item
