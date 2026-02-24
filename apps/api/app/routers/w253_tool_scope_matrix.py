"""Wave 253: Tool Scope Matrix UI v1 Router — Shows per-role tool scopes, sensitive data tiers, and required approvals. Matrix view with deterministic rendering and export capability.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w253_tool_scope_matrix import service

router = APIRouter(tags=["Tool Scope Matrix UI v1"])

@router.get("/api/tool-scope-matrix")
async def api_tool_scope_matrix_w253_list_matrices(limit: int = 100):
    """List tool scope matrices"""
    items = service.list_matrices(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tool-scope-matrix", status_code=201)
async def api_tool_scope_matrix_w253_create_matrix(request: Request):
    """Create tool scope matrix"""
    data = await request.json()
    item = service.create_matrix(data)
    return item

@router.get("/api/tool-scope-matrix/report")
async def api_tool_scope_matrix_w253_matrix_report(limit: int = 100):
    """Get tool scope matrix report"""
    items = service.matrix_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/tool-scope-matrix/{matrix_id}")
async def api_tool_scope_matrix_w253_get_matrix(matrix_id: str):
    """Get matrix details"""
    item = service.get_matrix(matrix_id)
    if not item:
        raise HTTPException(status_code=404, detail="tool_scope_matrix not found")
    return item

@router.post("/api/tool-scope-matrix/{matrix_id}/evaluate")
async def api_tool_scope_matrix_w253_evaluate_coverage(matrix_id: str, request: Request):
    """Evaluate scope coverage"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_coverage(matrix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tool_scope_matrix not found")
    return item

@router.post("/api/tool-scope-matrix/{matrix_id}/gaps")
async def api_tool_scope_matrix_w253_identify_gaps(matrix_id: str, request: Request):
    """Identify scope gaps"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.identify_gaps(matrix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tool_scope_matrix not found")
    return item
