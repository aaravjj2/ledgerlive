"""Wave 279: Ops Pack Export v1 Router — Signed bundle of channel interactions, approvals, incidents, and verify script. Deterministic export with content hash.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w279_ops_pack_export import service

router = APIRouter(tags=["Ops Pack Export v1"])

@router.get("/api/ops-pack-export")
async def api_ops_pack_export_w279_list_ops_packs(limit: int = 100):
    """List ops pack exports"""
    items = service.list_ops_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ops-pack-export", status_code=201)
async def api_ops_pack_export_w279_create_ops_pack(request: Request):
    """Create ops pack export"""
    data = await request.json()
    item = service.create_ops_pack(data)
    return item

@router.get("/api/ops-pack-export/report")
async def api_ops_pack_export_w279_ops_pack_report(limit: int = 100):
    """Get ops pack export report"""
    items = service.ops_pack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ops-pack-export/{ops_pack_id}")
async def api_ops_pack_export_w279_get_ops_pack(ops_pack_id: str):
    """Get ops pack details"""
    item = service.get_ops_pack(ops_pack_id)
    if not item:
        raise HTTPException(status_code=404, detail="ops_pack_export not found")
    return item

@router.post("/api/ops-pack-export/{ops_pack_id}/sign")
async def api_ops_pack_export_w279_sign_ops_pack(ops_pack_id: str, request: Request):
    """Sign ops pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_ops_pack(ops_pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ops_pack_export not found")
    return item

@router.post("/api/ops-pack-export/{ops_pack_id}/verify")
async def api_ops_pack_export_w279_verify_ops_pack(ops_pack_id: str, request: Request):
    """Verify ops pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_ops_pack(ops_pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ops_pack_export not found")
    return item
