"""Wave 72: Auto-Fix Actions Router — Approval-gated auto-fix actions with full audit trails for safe exception resolution.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w072_auto_fix import service

router = APIRouter(tags=["Auto-Fix Actions"])

@router.get("/api/auto-fixes")
async def api_auto_fix_w72_list_fixes(limit: int = 100):
    """List auto-fix actions"""
    items = service.list_fixes(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/auto-fixes", status_code=201)
async def api_auto_fix_w72_propose_fix(request: Request):
    """Propose an auto-fix"""
    data = await request.json()
    item = service.propose_fix(data)
    return item

@router.get("/api/auto-fixes/audit")
async def api_auto_fix_w72_fix_audit(limit: int = 100):
    """Get auto-fix audit log"""
    items = service.fix_audit(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/auto-fixes/{fix_id}")
async def api_auto_fix_w72_get_fix(fix_id: str):
    """Get fix details"""
    item = service.get_fix(fix_id)
    if not item:
        raise HTTPException(status_code=404, detail="auto_fix not found")
    return item

@router.post("/api/auto-fixes/{fix_id}/apply")
async def api_auto_fix_w72_apply_fix(fix_id: str, request: Request):
    """Apply approved fix"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_fix(fix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="auto_fix not found")
    return item

@router.post("/api/auto-fixes/{fix_id}/approve")
async def api_auto_fix_w72_approve_fix(fix_id: str, request: Request):
    """Approve auto-fix"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_fix(fix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="auto_fix not found")
    return item

@router.post("/api/auto-fixes/{fix_id}/rollback")
async def api_auto_fix_w72_rollback_fix(fix_id: str, request: Request):
    """Rollback applied fix"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback_fix(fix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="auto_fix not found")
    return item
