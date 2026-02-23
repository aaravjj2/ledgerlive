"""Wave 106: Compliance Bundle Signing Router — Compliance bundle signing with tamper verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w106_compliance_signing import service

router = APIRouter(tags=["Compliance Bundle Signing"])

@router.get("/api/compliance-signing")
async def api_compliance_signing_w106_list_bundles(limit: int = 100):
    """List signed compliance bundles"""
    items = service.list_bundles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/compliance-signing", status_code=201)
async def api_compliance_signing_w106_create_bundle(request: Request):
    """Create compliance bundle"""
    data = await request.json()
    item = service.create_bundle(data)
    return item

@router.get("/api/compliance-signing/export")
async def api_compliance_signing_w106_export_bundle(limit: int = 100):
    """Export signed bundle"""
    items = service.export_bundle(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/compliance-signing/{bundle_id}")
async def api_compliance_signing_w106_get_bundle(bundle_id: str):
    """Get bundle details"""
    item = service.get_bundle(bundle_id)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_signing not found")
    return item

@router.post("/api/compliance-signing/{bundle_id}/sign")
async def api_compliance_signing_w106_sign_bundle(bundle_id: str, request: Request):
    """Sign compliance bundle"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_bundle(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_signing not found")
    return item

@router.post("/api/compliance-signing/{bundle_id}/verify")
async def api_compliance_signing_w106_verify_tamper(bundle_id: str, request: Request):
    """Verify tamper resistance"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_tamper(bundle_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_signing not found")
    return item
