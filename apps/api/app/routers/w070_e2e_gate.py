"""Wave 70: E2E MCP Gate Router — Gate requiring make e2e:mcp:twice to pass. Proof pack demonstrates MCP coverage.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w070_e2e_gate import service

router = APIRouter(tags=["E2E MCP Gate"])

@router.get("/api/e2e-gates")
async def api_e2e_gate_w70_list_gates(limit: int = 100):
    """List E2E gate results"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/e2e-gates", status_code=201)
async def api_e2e_gate_w70_run_gate(request: Request):
    """Run E2E MCP gate"""
    data = await request.json()
    item = service.run_gate(data)
    return item

@router.get("/api/e2e-gates/report")
async def api_e2e_gate_w70_gate_report(limit: int = 100):
    """Get gate coverage report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/e2e-gates/{gate_id}")
async def api_e2e_gate_w70_get_gate(gate_id: str):
    """Get gate result details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="e2e_gate not found")
    return item

@router.post("/api/e2e-gates/{gate_id}/verify")
async def api_e2e_gate_w70_verify_determinism(gate_id: str, request: Request):
    """Verify determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="e2e_gate not found")
    return item
