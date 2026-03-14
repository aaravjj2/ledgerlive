"""Wave 338: Golden Scenario Gate v1 Router — Canonical dataset must produce blockers, approvals, incidents, replay regen equality, verified exports.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w338_golden_scenario_gate import service

router = APIRouter(tags=["Golden Scenario Gate v1"])

@router.get("/api/golden-scenario-gate")
async def api_golden_scenario_gate_w338_list_gates(limit: int = 100):
    """List golden scenario gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/golden-scenario-gate", status_code=201)
async def api_golden_scenario_gate_w338_run_gate(request: Request):
    """Run golden scenario gate"""
    data = await request.json()
    item = service.run_gate(data)
    return item

@router.get("/api/golden-scenario-gate/report")
async def api_golden_scenario_gate_w338_gate_report(limit: int = 100):
    """Get golden scenario report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/golden-scenario-gate/{gate_id}")
async def api_golden_scenario_gate_w338_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="golden_scenario_gate not found")
    return item

@router.post("/api/golden-scenario-gate/{gate_id}/evidence")
async def api_golden_scenario_gate_w338_export_evidence(gate_id: str, request: Request):
    """Export gate evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_evidence(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="golden_scenario_gate not found")
    return item

@router.post("/api/golden-scenario-gate/{gate_id}/verify")
async def api_golden_scenario_gate_w338_verify_conditions(gate_id: str, request: Request):
    """Verify all conditions met"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_conditions(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="golden_scenario_gate not found")
    return item
