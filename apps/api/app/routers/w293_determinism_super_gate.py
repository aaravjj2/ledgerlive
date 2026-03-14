"""Wave 293: Determinism Super Gate v1 Router — Run make test twice and compare deterministic artifacts with selected hashes that must match. Ultimate determinism verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w293_determinism_super_gate import service

router = APIRouter(tags=["Determinism Super Gate v1"])

@router.get("/api/determinism-super-gate")
async def api_determinism_super_gate_w293_list_super_gates(limit: int = 100):
    """List determinism super gates"""
    items = service.list_super_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/determinism-super-gate", status_code=201)
async def api_determinism_super_gate_w293_create_super_gate(request: Request):
    """Create determinism super gate"""
    data = await request.json()
    item = service.create_super_gate(data)
    return item

@router.get("/api/determinism-super-gate/report")
async def api_determinism_super_gate_w293_super_gate_report(limit: int = 100):
    """Get determinism super gate report"""
    items = service.super_gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/determinism-super-gate/{super_gate_id}")
async def api_determinism_super_gate_w293_get_super_gate(super_gate_id: str):
    """Get super gate details"""
    item = service.get_super_gate(super_gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="determinism_super_gate not found")
    return item

@router.post("/api/determinism-super-gate/{super_gate_id}/compare")
async def api_determinism_super_gate_w293_run_comparison(super_gate_id: str, request: Request):
    """Run hash comparison"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_comparison(super_gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="determinism_super_gate not found")
    return item

@router.post("/api/determinism-super-gate/{super_gate_id}/select")
async def api_determinism_super_gate_w293_select_artifacts(super_gate_id: str, request: Request):
    """Select artifacts to compare"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.select_artifacts(super_gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="determinism_super_gate not found")
    return item
