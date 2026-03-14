"""Wave 188: Live-Mode Audit Sealing v1 Router — Extended Merkle audit integrity including tool_trace and live session events. Binder bundles include integrity proof for tool traces. Tamper detection.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w188_audit_seal import service

router = APIRouter(tags=["Live-Mode Audit Sealing v1"])

@router.get("/api/audit-seal")
async def api_audit_seal_w188_list_seals(limit: int = 100):
    """List audit seals"""
    items = service.list_seals(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-seal", status_code=201)
async def api_audit_seal_w188_create_seal(request: Request):
    """Create audit seal with Merkle proof"""
    data = await request.json()
    item = service.create_seal(data)
    return item

@router.get("/api/audit-seal/report")
async def api_audit_seal_w188_seal_report(limit: int = 100):
    """Get audit seal report"""
    items = service.seal_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/audit-seal/{seal_id}")
async def api_audit_seal_w188_get_seal(seal_id: str):
    """Get seal details"""
    item = service.get_seal(seal_id)
    if not item:
        raise HTTPException(status_code=404, detail="audit_seal not found")
    return item

@router.post("/api/audit-seal/{seal_id}/detect")
async def api_audit_seal_w188_detect_tamper(seal_id: str, request: Request):
    """Detect tampering"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.detect_tamper(seal_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_seal not found")
    return item

@router.post("/api/audit-seal/{seal_id}/tamper")
async def api_audit_seal_w188_inject_tamper(seal_id: str, request: Request):
    """Inject tamper for testing"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.inject_tamper(seal_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_seal not found")
    return item

@router.post("/api/audit-seal/{seal_id}/verify")
async def api_audit_seal_w188_verify_integrity(seal_id: str, request: Request):
    """Verify Merkle integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_integrity(seal_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_seal not found")
    return item
