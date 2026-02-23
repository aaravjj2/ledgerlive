"""Wave 212: Binder Regeneration From Replay Router — Regenerate binder and board pack from replay artifacts. Must be byte-identical to original exports. Hard gate on hash equality.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w212_binder_regen import service

router = APIRouter(tags=["Binder Regeneration From Replay"])

@router.get("/api/binder-regen")
async def api_binder_regen_w212_list_regens(limit: int = 100):
    """List binder regenerations"""
    items = service.list_regens(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/binder-regen", status_code=201)
async def api_binder_regen_w212_regenerate(request: Request):
    """Regenerate binder from replay"""
    data = await request.json()
    item = service.regenerate(data)
    return item

@router.get("/api/binder-regen/report")
async def api_binder_regen_w212_regen_report(limit: int = 100):
    """Get binder regeneration report"""
    items = service.regen_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/binder-regen/{regen_id}")
async def api_binder_regen_w212_get_regen(regen_id: str):
    """Get regeneration details"""
    item = service.get_regen(regen_id)
    if not item:
        raise HTTPException(status_code=404, detail="binder_regen not found")
    return item

@router.post("/api/binder-regen/{regen_id}/compare")
async def api_binder_regen_w212_compare_hashes(regen_id: str, request: Request):
    """Compare original vs regen hashes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare_hashes(regen_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="binder_regen not found")
    return item

@router.post("/api/binder-regen/{regen_id}/verify")
async def api_binder_regen_w212_verify_identity(regen_id: str, request: Request):
    """Verify byte-identical match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_identity(regen_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="binder_regen not found")
    return item
