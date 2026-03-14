"""Wave 275: Cross-Channel Audit v1 Router — Every channel action writes audit and tool trace with dossier updates. Full cross-channel audit trail with deterministic ordering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w275_cross_channel_audit import service

router = APIRouter(tags=["Cross-Channel Audit v1"])

@router.get("/api/cross-channel-audit")
async def api_cross_channel_audit_w275_list_audit_entries(limit: int = 100):
    """List cross-channel audit entries"""
    items = service.list_audit_entries(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/cross-channel-audit", status_code=201)
async def api_cross_channel_audit_w275_create_audit_entry(request: Request):
    """Create cross-channel audit entry"""
    data = await request.json()
    item = service.create_audit_entry(data)
    return item

@router.get("/api/cross-channel-audit/report")
async def api_cross_channel_audit_w275_audit_entry_report(limit: int = 100):
    """Get cross-channel audit report"""
    items = service.audit_entry_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cross-channel-audit/{audit_entry_id}")
async def api_cross_channel_audit_w275_get_audit_entry(audit_entry_id: str):
    """Get audit entry details"""
    item = service.get_audit_entry(audit_entry_id)
    if not item:
        raise HTTPException(status_code=404, detail="cross_channel_audit not found")
    return item

@router.post("/api/cross-channel-audit/{audit_entry_id}/dossier")
async def api_cross_channel_audit_w275_update_dossier(audit_entry_id: str, request: Request):
    """Update linked dossier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.update_dossier(audit_entry_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cross_channel_audit not found")
    return item

@router.post("/api/cross-channel-audit/{audit_entry_id}/trace")
async def api_cross_channel_audit_w275_link_trace(audit_entry_id: str, request: Request):
    """Link tool trace"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_trace(audit_entry_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cross_channel_audit not found")
    return item
