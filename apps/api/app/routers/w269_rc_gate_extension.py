"""Wave 269: RC Gate Extension v1 Router — Court, replay, and telemetry packs must verify. Drift budgets must pass. Extended gate checking for Race Control release readiness.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w269_rc_gate_extension import service

router = APIRouter(tags=["RC Gate Extension v1"])

@router.get("/api/rc-gate-extension")
async def api_rc_gate_extension_w269_list_gate_exts(limit: int = 100):
    """List RC gate extensions"""
    items = service.list_gate_exts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-gate-extension", status_code=201)
async def api_rc_gate_extension_w269_create_gate_ext(request: Request):
    """Create RC gate extension check"""
    data = await request.json()
    item = service.create_gate_ext(data)
    return item

@router.get("/api/rc-gate-extension/report")
async def api_rc_gate_extension_w269_gate_ext_report(limit: int = 100):
    """Get RC gate extension report"""
    items = service.gate_ext_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-gate-extension/{gate_ext_id}")
async def api_rc_gate_extension_w269_get_gate_ext(gate_ext_id: str):
    """Get gate extension details"""
    item = service.get_gate_ext(gate_ext_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_extension not found")
    return item

@router.post("/api/rc-gate-extension/{gate_ext_id}/drift")
async def api_rc_gate_extension_w269_check_drift(gate_ext_id: str, request: Request):
    """Check drift budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_drift(gate_ext_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_extension not found")
    return item

@router.post("/api/rc-gate-extension/{gate_ext_id}/evaluate")
async def api_rc_gate_extension_w269_evaluate_all(gate_ext_id: str, request: Request):
    """Evaluate all gate checks"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_all(gate_ext_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_gate_extension not found")
    return item
