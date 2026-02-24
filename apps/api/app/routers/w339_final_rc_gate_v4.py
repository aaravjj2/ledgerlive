"""Wave 339: Final RC Gate v4 Router — Asserts builder coverage, Atlassian mocks, Airia readiness, security budgets, Golden Scenario PASS.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w339_final_rc_gate_v4 import service

router = APIRouter(tags=["Final RC Gate v4"])

@router.get("/api/final-rc-gate-v4")
async def api_final_rc_gate_v4_w339_list_gates(limit: int = 100):
    """List final RC gates v4"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/final-rc-gate-v4", status_code=201)
async def api_final_rc_gate_v4_w339_run_gate(request: Request):
    """Run final RC gate v4"""
    data = await request.json()
    item = service.run_gate(data)
    return item

@router.get("/api/final-rc-gate-v4/report")
async def api_final_rc_gate_v4_w339_gate_report(limit: int = 100):
    """Get final RC gate report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/final-rc-gate-v4/{gate_id}")
async def api_final_rc_gate_v4_w339_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="final_rc_gate_v4 not found")
    return item

@router.post("/api/final-rc-gate-v4/{gate_id}/export")
async def api_final_rc_gate_v4_w339_export_gate_pack(gate_id: str, request: Request):
    """Export gate results pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_gate_pack(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="final_rc_gate_v4 not found")
    return item

@router.post("/api/final-rc-gate-v4/{gate_id}/verify")
async def api_final_rc_gate_v4_w339_verify_all(gate_id: str, request: Request):
    """Verify all sub-gates"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_all(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="final_rc_gate_v4 not found")
    return item
