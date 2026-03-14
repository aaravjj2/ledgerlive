"""Wave 19: Audit Integrity Router — Merkle-tree audit log integrity verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w19_audit_integrity import service

router = APIRouter(tags=["Audit Integrity"])

@router.get("/api/audit-integrity/checks")
async def api_list_checks(limit: int = 100):
    """List integrity checks"""
    items = service.list_checks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-integrity/hash", status_code=201)
async def api_compute_hash(request: Request):
    """Compute hash for range"""
    data = await request.json()
    item = service.compute_hash(data)
    return item

@router.get("/api/audit-integrity/stats")
async def api_stats(limit: int = 100):
    """Integrity statistics"""
    items = service.stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-integrity/verify", status_code=201)
async def api_verify(request: Request):
    """Run integrity check"""
    data = await request.json()
    item = service.verify(data)
    return item

@router.get("/api/audit-integrity/checks/{check_id}")
async def api_get_check(check_id: str):
    """Get check details"""
    item = service.get_check(check_id)
    if not item:
        raise HTTPException(status_code=404, detail="audit_integrity not found")
    return item
