"""Wave 258: Security Posture Pack v1 Router — Signed export with events, proofs, and verifier outputs. Byte-identical determinism for reproducible security posture snapshots.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w258_security_posture_pack import service

router = APIRouter(tags=["Security Posture Pack v1"])

@router.get("/api/security-posture-pack")
async def api_security_posture_pack_w258_list_packs(limit: int = 100):
    """List security posture packs"""
    items = service.list_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-posture-pack", status_code=201)
async def api_security_posture_pack_w258_create_pack(request: Request):
    """Create security posture pack"""
    data = await request.json()
    item = service.create_pack(data)
    return item

@router.get("/api/security-posture-pack/report")
async def api_security_posture_pack_w258_pack_report(limit: int = 100):
    """Get security posture pack report"""
    items = service.pack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-posture-pack/{pack_id}")
async def api_security_posture_pack_w258_get_pack(pack_id: str):
    """Get pack details"""
    item = service.get_pack(pack_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_posture_pack not found")
    return item

@router.post("/api/security-posture-pack/{pack_id}/sign")
async def api_security_posture_pack_w258_sign_pack(pack_id: str, request: Request):
    """Sign posture pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_posture_pack not found")
    return item

@router.post("/api/security-posture-pack/{pack_id}/verify")
async def api_security_posture_pack_w258_verify_pack(pack_id: str, request: Request):
    """Verify pack integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_posture_pack not found")
    return item
