"""Wave 128: Access Change Audit Router — Audit portal enhancements for tracking access changes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w128_access_audit import service

router = APIRouter(tags=["Access Change Audit"])

@router.get("/api/access-audits")
async def api_access_audit_w128_list_audits(limit: int = 100):
    """List access change audits"""
    items = service.list_audits(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/access-audits", status_code=201)
async def api_access_audit_w128_record_change(request: Request):
    """Record access change"""
    data = await request.json()
    item = service.record_change(data)
    return item

@router.get("/api/access-audits/report")
async def api_access_audit_w128_audit_report(limit: int = 100):
    """Get access audit report"""
    items = service.audit_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/access-audits/timeline")
async def api_access_audit_w128_access_timeline(limit: int = 100):
    """Get access change timeline"""
    items = service.access_timeline(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/access-audits/{audit_id}")
async def api_access_audit_w128_get_audit(audit_id: str):
    """Get audit details"""
    item = service.get_audit(audit_id)
    if not item:
        raise HTTPException(status_code=404, detail="access_audit not found")
    return item

@router.post("/api/access-audits/{audit_id}/revert")
async def api_access_audit_w128_revert_change(audit_id: str, request: Request):
    """Revert access change"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.revert_change(audit_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="access_audit not found")
    return item
