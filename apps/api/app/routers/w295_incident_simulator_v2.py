"""Wave 295: Incident Simulator v2 Router — Seeded incident scenarios including policy blocks, channel failures, and drift breach with deterministic playbooks.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w295_incident_simulator_v2 import service

router = APIRouter(tags=["Incident Simulator v2"])

@router.get("/api/incident-simulator-v2")
async def api_incident_simulator_v2_w295_list_simulators(limit: int = 100):
    """List incident simulators"""
    items = service.list_simulators(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/incident-simulator-v2", status_code=201)
async def api_incident_simulator_v2_w295_create_simulator(request: Request):
    """Create incident simulator"""
    data = await request.json()
    item = service.create_simulator(data)
    return item

@router.get("/api/incident-simulator-v2/report")
async def api_incident_simulator_v2_w295_simulator_report(limit: int = 100):
    """Get incident simulator report"""
    items = service.simulator_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/incident-simulator-v2/{simulator_id}")
async def api_incident_simulator_v2_w295_get_simulator(simulator_id: str):
    """Get simulator details"""
    item = service.get_simulator(simulator_id)
    if not item:
        raise HTTPException(status_code=404, detail="incident_simulator_v2 not found")
    return item

@router.post("/api/incident-simulator-v2/{simulator_id}/playbook")
async def api_incident_simulator_v2_w295_trigger_playbook(simulator_id: str, request: Request):
    """Trigger recovery playbook"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.trigger_playbook(simulator_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_simulator_v2 not found")
    return item

@router.post("/api/incident-simulator-v2/{simulator_id}/run")
async def api_incident_simulator_v2_w295_run_scenario(simulator_id: str, request: Request):
    """Run incident scenario"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_scenario(simulator_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_simulator_v2 not found")
    return item

@router.post("/api/incident-simulator-v2/{simulator_id}/verify")
async def api_incident_simulator_v2_w295_verify_outcome(simulator_id: str, request: Request):
    """Verify scenario outcome"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_outcome(simulator_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_simulator_v2 not found")
    return item
