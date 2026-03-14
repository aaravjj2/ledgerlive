"""Wave 337: Unified Why/Verify UX v4 Router — One-click dossier/evidence/policy from every table row.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w337_unified_why_verify_v4 import service

router = APIRouter(tags=["Unified Why/Verify UX v4"])

@router.get("/api/unified-why-verify-v4")
async def api_unified_why_verify_v4_w337_list_verifications(limit: int = 100):
    """List verifications"""
    items = service.list_verifications(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/unified-why-verify-v4", status_code=201)
async def api_unified_why_verify_v4_w337_create_verification(request: Request):
    """Create verification"""
    data = await request.json()
    item = service.create_verification(data)
    return item

@router.get("/api/unified-why-verify-v4/report")
async def api_unified_why_verify_v4_w337_verify_report(limit: int = 100):
    """Get verification report"""
    items = service.verify_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/unified-why-verify-v4/{verify_id}")
async def api_unified_why_verify_v4_w337_get_verification(verify_id: str):
    """Get verification details"""
    item = service.get_verification(verify_id)
    if not item:
        raise HTTPException(status_code=404, detail="unified_why_verify_v4 not found")
    return item

@router.post("/api/unified-why-verify-v4/{verify_id}/dossier")
async def api_unified_why_verify_v4_w337_fetch_dossier(verify_id: str, request: Request):
    """Fetch linked dossier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.fetch_dossier(verify_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="unified_why_verify_v4 not found")
    return item

@router.post("/api/unified-why-verify-v4/{verify_id}/evidence")
async def api_unified_why_verify_v4_w337_fetch_evidence(verify_id: str, request: Request):
    """Fetch linked evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.fetch_evidence(verify_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="unified_why_verify_v4 not found")
    return item
