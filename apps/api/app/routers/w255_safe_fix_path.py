"""Wave 255: Safe Fix Path v1 Router — Blocked actions show evidence-backed remediation suggestions with no side effects until approved. Deterministic suggestion generation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w255_safe_fix_path import service

router = APIRouter(tags=["Safe Fix Path v1"])

@router.get("/api/safe-fix-path")
async def api_safe_fix_path_w255_list_fixes(limit: int = 100):
    """List safe fix paths"""
    items = service.list_fixes(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/safe-fix-path", status_code=201)
async def api_safe_fix_path_w255_suggest_fix(request: Request):
    """Suggest safe fix path"""
    data = await request.json()
    item = service.suggest_fix(data)
    return item

@router.get("/api/safe-fix-path/report")
async def api_safe_fix_path_w255_fix_report(limit: int = 100):
    """Get safe fix path report"""
    items = service.fix_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/safe-fix-path/{fix_id}")
async def api_safe_fix_path_w255_get_fix(fix_id: str):
    """Get fix path details"""
    item = service.get_fix(fix_id)
    if not item:
        raise HTTPException(status_code=404, detail="safe_fix_path not found")
    return item

@router.post("/api/safe-fix-path/{fix_id}/apply")
async def api_safe_fix_path_w255_apply_fix(fix_id: str, request: Request):
    """Apply approved fix"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_fix(fix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="safe_fix_path not found")
    return item

@router.post("/api/safe-fix-path/{fix_id}/approve")
async def api_safe_fix_path_w255_approve_fix(fix_id: str, request: Request):
    """Approve fix path"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_fix(fix_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="safe_fix_path not found")
    return item
