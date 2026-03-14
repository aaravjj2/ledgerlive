"""Wave 263: Telemetry Pack v3 Router — Combines tool trace, verifier checks, drift snapshot, incidents, and security timeline into a deterministic zip with content verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w263_telemetry_pack_v3 import service

router = APIRouter(tags=["Telemetry Pack v3"])

@router.get("/api/telemetry-pack-v3")
async def api_telemetry_pack_v3_w263_list_packs(limit: int = 100):
    """List telemetry packs"""
    items = service.list_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/telemetry-pack-v3", status_code=201)
async def api_telemetry_pack_v3_w263_create_pack(request: Request):
    """Create telemetry pack"""
    data = await request.json()
    item = service.create_pack(data)
    return item

@router.get("/api/telemetry-pack-v3/report")
async def api_telemetry_pack_v3_w263_pack_report(limit: int = 100):
    """Get telemetry pack report"""
    items = service.pack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/telemetry-pack-v3/{pack_id}")
async def api_telemetry_pack_v3_w263_get_pack(pack_id: str):
    """Get telemetry pack details"""
    item = service.get_pack(pack_id)
    if not item:
        raise HTTPException(status_code=404, detail="telemetry_pack_v3 not found")
    return item

@router.post("/api/telemetry-pack-v3/{pack_id}/component")
async def api_telemetry_pack_v3_w263_add_component(pack_id: str, request: Request):
    """Add component to pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_component(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="telemetry_pack_v3 not found")
    return item

@router.post("/api/telemetry-pack-v3/{pack_id}/verify")
async def api_telemetry_pack_v3_w263_verify_pack(pack_id: str, request: Request):
    """Verify telemetry pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="telemetry_pack_v3 not found")
    return item
