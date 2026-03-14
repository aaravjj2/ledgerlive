"""Wave 104: GDPR Redaction 2.0 Router — GDPR-compliant redaction preserving Merkle audit integrity.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w104_gdpr_redaction import service

router = APIRouter(tags=["GDPR Redaction 2.0"])

@router.get("/api/gdpr-redactions")
async def api_gdpr_redaction_w104_list_redactions(limit: int = 100):
    """List GDPR redactions"""
    items = service.list_redactions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gdpr-redactions", status_code=201)
async def api_gdpr_redaction_w104_create_redaction(request: Request):
    """Create redaction request"""
    data = await request.json()
    item = service.create_redaction(data)
    return item

@router.get("/api/gdpr-redactions/report")
async def api_gdpr_redaction_w104_redaction_report(limit: int = 100):
    """Get redaction report"""
    items = service.redaction_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gdpr-redactions/{redaction_id}")
async def api_gdpr_redaction_w104_get_redaction(redaction_id: str):
    """Get redaction details"""
    item = service.get_redaction(redaction_id)
    if not item:
        raise HTTPException(status_code=404, detail="gdpr_redaction not found")
    return item

@router.post("/api/gdpr-redactions/{redaction_id}/execute")
async def api_gdpr_redaction_w104_execute_redaction(redaction_id: str, request: Request):
    """Execute redaction"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.execute_redaction(redaction_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gdpr_redaction not found")
    return item

@router.post("/api/gdpr-redactions/{redaction_id}/verify")
async def api_gdpr_redaction_w104_verify_integrity(redaction_id: str, request: Request):
    """Verify Merkle integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_integrity(redaction_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gdpr_redaction not found")
    return item
