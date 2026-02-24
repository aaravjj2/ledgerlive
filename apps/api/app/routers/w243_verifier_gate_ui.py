"""Wave 243: Verifier Gate UI v1 Router — Shows which invariants pass or fail, surfaces required approvals per step, and provides deterministic deny reasons for blocked actions.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w243_verifier_gate_ui import service

router = APIRouter(tags=["Verifier Gate UI v1"])

@router.get("/api/verifier-gate")
async def api_verifier_gate_ui_w243_list_gates(limit: int = 100):
    """List verifier gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/verifier-gate", status_code=201)
async def api_verifier_gate_ui_w243_create_gate(request: Request):
    """Create verifier gate evaluation"""
    data = await request.json()
    item = service.create_gate(data)
    return item

@router.get("/api/verifier-gate/report")
async def api_verifier_gate_ui_w243_gate_report(limit: int = 100):
    """Get verifier gate report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/verifier-gate/{gate_id}")
async def api_verifier_gate_ui_w243_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="verifier_gate_ui not found")
    return item

@router.post("/api/verifier-gate/{gate_id}/evaluate")
async def api_verifier_gate_ui_w243_evaluate_gate(gate_id: str, request: Request):
    """Evaluate gate invariants"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_gate(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="verifier_gate_ui not found")
    return item

@router.post("/api/verifier-gate/{gate_id}/explain-deny")
async def api_verifier_gate_ui_w243_explain_deny(gate_id: str, request: Request):
    """Explain deny reasons"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.explain_deny(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="verifier_gate_ui not found")
    return item
