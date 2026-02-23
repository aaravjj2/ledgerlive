"""Wave 116: DQ Export Gate Router — Data quality gates that block exports unless approved.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w116_dq_export_gate import service

router = APIRouter(tags=["DQ Export Gate"])

@router.get("/api/dq-export-gates")
async def api_dq_export_gate_w116_list_gates(limit: int = 100):
    """List DQ export gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/dq-export-gates", status_code=201)
async def api_dq_export_gate_w116_check_gate(request: Request):
    """Check DQ export gate"""
    data = await request.json()
    item = service.check_gate(data)
    return item

@router.get("/api/dq-export-gates/report")
async def api_dq_export_gate_w116_gate_report(limit: int = 100):
    """Get DQ gate report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/dq-export-gates/{gate_id}")
async def api_dq_export_gate_w116_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="dq_export_gate not found")
    return item

@router.post("/api/dq-export-gates/{gate_id}/approve")
async def api_dq_export_gate_w116_approve_override(gate_id: str, request: Request):
    """Approve export override"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_override(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="dq_export_gate not found")
    return item
