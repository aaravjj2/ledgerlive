"""Wave 127: Export Permission Gate Router — Export permission gates with audited access control.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w127_export_perm_gate import service

router = APIRouter(tags=["Export Permission Gate"])

@router.get("/api/export-perm-gates")
async def api_export_perm_gate_w127_list_gates(limit: int = 100):
    """List export permission gates"""
    items = service.list_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/export-perm-gates", status_code=201)
async def api_export_perm_gate_w127_check_permission(request: Request):
    """Check export permission"""
    data = await request.json()
    item = service.check_permission(data)
    return item

@router.get("/api/export-perm-gates/report")
async def api_export_perm_gate_w127_gate_report(limit: int = 100):
    """Get export permission report"""
    items = service.gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/export-perm-gates/{gate_id}")
async def api_export_perm_gate_w127_get_gate(gate_id: str):
    """Get gate details"""
    item = service.get_gate(gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="export_perm_gate not found")
    return item

@router.post("/api/export-perm-gates/{gate_id}/audit")
async def api_export_perm_gate_w127_audit_access(gate_id: str, request: Request):
    """Audit access attempt"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.audit_access(gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="export_perm_gate not found")
    return item
