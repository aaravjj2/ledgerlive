"""Wave 152: Hash Equality Gate Router — Generate release twice → identical hash equality hard gate.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w152_hash_equality_gate import service

router = APIRouter(tags=["Hash Equality Gate"])

@router.get("/api/hash-equality-gates")
async def api_hash_equality_gate_w152_list_gates(limit: int = 100):
    """List hash equality gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/hash-equality-gates", status_code=201)
async def api_hash_equality_gate_w152_run_gate(request: Request):
    """Run hash equality gate"""
    data = await request.json()
    item = service.run_gate(data)
    return item

@router.get("/api/hash-equality-gates/report")
async def api_hash_equality_gate_w152_gate_report(limit: int = 100):
    """Get hash equality report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/hash-equality-gates/{gate_id}")
async def api_hash_equality_gate_w152_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="hash_equality_gate not found")
    return item

@router.post("/api/hash-equality-gates/{gate_id}/verify")
async def api_hash_equality_gate_w152_verify_equality(gate_id: str, request: Request):
    """Verify hash equality"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_equality(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="hash_equality_gate not found")
    return item
