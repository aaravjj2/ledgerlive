"""Wave 297: Documentation Truth Gate v1 Router — README, VERIFY, and route registry must match Make targets and live endpoints. Deterministic documentation checks.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w297_doc_truth_gate import service

router = APIRouter(tags=["Documentation Truth Gate v1"])

@router.get("/api/doc-truth-gate")
async def api_doc_truth_gate_w297_list_truth_gates(limit: int = 100):
    """List documentation truth gates"""
    items = service.list_truth_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/doc-truth-gate", status_code=201)
async def api_doc_truth_gate_w297_create_truth_gate(request: Request):
    """Create documentation truth gate"""
    data = await request.json()
    item = service.create_truth_gate(data)
    return item

@router.get("/api/doc-truth-gate/report")
async def api_doc_truth_gate_w297_truth_gate_report(limit: int = 100):
    """Get documentation truth gate report"""
    items = service.truth_gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/doc-truth-gate/{truth_gate_id}")
async def api_doc_truth_gate_w297_get_truth_gate(truth_gate_id: str):
    """Get truth gate details"""
    item = service.get_truth_gate(truth_gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="doc_truth_gate not found")
    return item

@router.post("/api/doc-truth-gate/{truth_gate_id}/readme")
async def api_doc_truth_gate_w297_check_readme(truth_gate_id: str, request: Request):
    """Check README accuracy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_readme(truth_gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="doc_truth_gate not found")
    return item

@router.post("/api/doc-truth-gate/{truth_gate_id}/routes")
async def api_doc_truth_gate_w297_check_routes(truth_gate_id: str, request: Request):
    """Check route registry"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_routes(truth_gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="doc_truth_gate not found")
    return item
