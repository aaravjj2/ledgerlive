"""Wave 262: Court Pack v4 Router — Generated directly from Race Control. Includes offline viewer, verify-all script, and parity report attachments with deterministic content.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w262_court_pack_v4 import service

router = APIRouter(tags=["Court Pack v4"])

@router.get("/api/court-pack-v4")
async def api_court_pack_v4_w262_list_packs(limit: int = 100):
    """List court packs"""
    items = service.list_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/court-pack-v4", status_code=201)
async def api_court_pack_v4_w262_create_pack(request: Request):
    """Create court pack from RC"""
    data = await request.json()
    item = service.create_pack(data)
    return item

@router.get("/api/court-pack-v4/report")
async def api_court_pack_v4_w262_pack_report(limit: int = 100):
    """Get court pack report"""
    items = service.pack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/court-pack-v4/{pack_id}")
async def api_court_pack_v4_w262_get_pack(pack_id: str):
    """Get court pack details"""
    item = service.get_pack(pack_id)
    if not item:
        raise HTTPException(status_code=404, detail="court_pack_v4 not found")
    return item

@router.post("/api/court-pack-v4/{pack_id}/parity")
async def api_court_pack_v4_w262_attach_parity(pack_id: str, request: Request):
    """Attach parity report"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.attach_parity(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="court_pack_v4 not found")
    return item

@router.post("/api/court-pack-v4/{pack_id}/verify")
async def api_court_pack_v4_w262_verify_pack(pack_id: str, request: Request):
    """Verify court pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="court_pack_v4 not found")
    return item
