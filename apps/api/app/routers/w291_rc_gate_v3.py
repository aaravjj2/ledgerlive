"""Wave 291: RC Gate v3 Router — Unified release candidate run asserting all critical invariants across Race Control, channels, replay, security, ML, and exports.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w291_rc_gate_v3 import service

router = APIRouter(tags=["RC Gate v3"])

@router.get("/api/rc-gate-v3")
async def api_rc_gate_v3_w291_list_gates(limit: int = 100):
    """List RC gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-gate-v3", status_code=201)
async def api_rc_gate_v3_w291_create_gate(request: Request):
    """Create RC gate evaluation"""
    data = await request.json()
    item = service.create_gate(data)
    return item

@router.get("/api/rc-gate-v3/report")
async def api_rc_gate_v3_w291_gate_report(limit: int = 100):
    """Get RC gate report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-gate-v3/{gate_id}")
async def api_rc_gate_v3_w291_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_v3 not found")
    return item

@router.post("/api/rc-gate-v3/{gate_id}/channels")
async def api_rc_gate_v3_w291_check_channels(gate_id: str, request: Request):
    """Check channel invariants"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_channels(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_v3 not found")
    return item

@router.post("/api/rc-gate-v3/{gate_id}/evaluate")
async def api_rc_gate_v3_w291_evaluate_all(gate_id: str, request: Request):
    """Evaluate all invariants"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_all(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_v3 not found")
    return item

@router.post("/api/rc-gate-v3/{gate_id}/security")
async def api_rc_gate_v3_w291_check_security(gate_id: str, request: Request):
    """Check security invariants"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_security(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_v3 not found")
    return item
