"""Wave 139: Offline Incident Simulator Router — Offline incident simulation with deterministic reports.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w139_incident_sim import service

router = APIRouter(tags=["Offline Incident Simulator"])

@router.get("/api/incident-sims")
async def api_incident_sim_w139_list_incidents(limit: int = 100):
    """List incident simulations"""
    items = service.list_incidents(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/incident-sims", status_code=201)
async def api_incident_sim_w139_simulate(request: Request):
    """Run incident simulation"""
    data = await request.json()
    item = service.simulate(data)
    return item

@router.get("/api/incident-sims/report")
async def api_incident_sim_w139_sim_report(limit: int = 100):
    """Get simulation report"""
    items = service.sim_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/incident-sims/{incident_id}")
async def api_incident_sim_w139_get_incident(incident_id: str):
    """Get simulation details"""
    item = service.get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="incident_sim not found")
    return item

@router.post("/api/incident-sims/{incident_id}/assess")
async def api_incident_sim_w139_assess_impact(incident_id: str, request: Request):
    """Assess incident impact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assess_impact(incident_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_sim not found")
    return item

@router.post("/api/incident-sims/{incident_id}/resolve")
async def api_incident_sim_w139_resolution_plan(incident_id: str, request: Request):
    """Generate resolution plan"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolution_plan(incident_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_sim not found")
    return item
