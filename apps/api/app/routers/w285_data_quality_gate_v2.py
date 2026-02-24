"""Wave 285: Data Quality Gate v2 Router — Export blocked if quality below threshold unless approved. Deterministic quality scoring with explicit reasons.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w285_data_quality_gate_v2 import service

router = APIRouter(tags=["Data Quality Gate v2"])

@router.get("/api/data-quality-gate-v2")
async def api_data_quality_gate_v2_w285_list_gates(limit: int = 100):
    """List data quality gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/data-quality-gate-v2", status_code=201)
async def api_data_quality_gate_v2_w285_create_gate(request: Request):
    """Create data quality gate"""
    data = await request.json()
    item = service.create_gate(data)
    return item

@router.get("/api/data-quality-gate-v2/report")
async def api_data_quality_gate_v2_w285_gate_report(limit: int = 100):
    """Get data quality gate report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-quality-gate-v2/{gate_id}")
async def api_data_quality_gate_v2_w285_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_quality_gate_v2 not found")
    return item

@router.post("/api/data-quality-gate-v2/{gate_id}/evaluate")
async def api_data_quality_gate_v2_w285_evaluate_quality(gate_id: str, request: Request):
    """Evaluate data quality"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_quality(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_quality_gate_v2 not found")
    return item

@router.post("/api/data-quality-gate-v2/{gate_id}/override")
async def api_data_quality_gate_v2_w285_override_gate(gate_id: str, request: Request):
    """Override gate with approval"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.override_gate(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_quality_gate_v2 not found")
    return item
