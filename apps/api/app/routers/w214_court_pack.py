"""Wave 214: Audit Court Mode Export v1 Router — Single zip: original binder+sig, replay binder+sig, parity report, transcript pack, explanation graph, audit integrity proof. VERIFY script validates offline.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w214_court_pack import service

router = APIRouter(tags=["Audit Court Mode Export v1"])

@router.get("/api/court-pack")
async def api_court_pack_w214_list_packs(limit: int = 100):
    """List court mode export packs"""
    items = service.list_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/court-pack", status_code=201)
async def api_court_pack_w214_generate_pack(request: Request):
    """Generate court mode export pack"""
    data = await request.json()
    item = service.generate_pack(data)
    return item

@router.get("/api/court-pack/report")
async def api_court_pack_w214_pack_report(limit: int = 100):
    """Get court pack report"""
    items = service.pack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/court-pack/{pack_id}")
async def api_court_pack_w214_get_pack(pack_id: str):
    """Get pack details"""
    item = service.get_pack(pack_id)
    if not item:
        raise HTTPException(status_code=404, detail="court_pack not found")
    return item

@router.post("/api/court-pack/{pack_id}/download")
async def api_court_pack_w214_download_pack(pack_id: str, request: Request):
    """Download court pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.download_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="court_pack not found")
    return item

@router.post("/api/court-pack/{pack_id}/verify")
async def api_court_pack_w214_verify_pack(pack_id: str, request: Request):
    """Verify all checksums and signatures"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="court_pack not found")
    return item
