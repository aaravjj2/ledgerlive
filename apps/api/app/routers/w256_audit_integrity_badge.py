"""Wave 256: Audit Integrity Badge v1 Router — Race Control shows Merkle proof status for audit, tool trace, and security events. Badge indicates verified, unverified, or tampered state.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w256_audit_integrity_badge import service

router = APIRouter(tags=["Audit Integrity Badge v1"])

@router.get("/api/audit-integrity-badge")
async def api_audit_integrity_badge_w256_list_badges(limit: int = 100):
    """List integrity badges"""
    items = service.list_badges(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-integrity-badge", status_code=201)
async def api_audit_integrity_badge_w256_create_badge(request: Request):
    """Create integrity badge"""
    data = await request.json()
    item = service.create_badge(data)
    return item

@router.get("/api/audit-integrity-badge/report")
async def api_audit_integrity_badge_w256_badge_report(limit: int = 100):
    """Get integrity badge report"""
    items = service.badge_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/audit-integrity-badge/{badge_id}")
async def api_audit_integrity_badge_w256_get_badge(badge_id: str):
    """Get badge details"""
    item = service.get_badge(badge_id)
    if not item:
        raise HTTPException(status_code=404, detail="audit_integrity_badge not found")
    return item

@router.post("/api/audit-integrity-badge/{badge_id}/recompute")
async def api_audit_integrity_badge_w256_recompute_badge(badge_id: str, request: Request):
    """Recompute Merkle proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recompute_badge(badge_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_integrity_badge not found")
    return item

@router.post("/api/audit-integrity-badge/{badge_id}/verify")
async def api_audit_integrity_badge_w256_verify_badge(badge_id: str, request: Request):
    """Verify badge integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_badge(badge_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_integrity_badge not found")
    return item
