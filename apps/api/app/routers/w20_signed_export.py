"""Wave 20: Signed Exports Router — Cryptographically signed document and report exports.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w20_signed_export import service

router = APIRouter(tags=["Signed Exports"])

@router.get("/api/exports")
async def api_list(limit: int = 100):
    """List exports"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/exports", status_code=201)
async def api_create(request: Request):
    """Create a signed export"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/exports/{export_id}")
async def api_get(export_id: str):
    """Get export details"""
    item = service.get(export_id)
    if not item:
        raise HTTPException(status_code=404, detail="signed_export not found")
    return item

@router.get("/api/exports/{export_id}/download")
async def api_download(export_id: str):
    """Download export"""
    item = service.download(export_id)
    if not item:
        raise HTTPException(status_code=404, detail="signed_export not found")
    return item

@router.post("/api/exports/{export_id}/verify")
async def api_verify_sig(export_id: str, request: Request):
    """Verify export signature"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_sig(export_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="signed_export not found")
    return item
