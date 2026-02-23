"""Wave 9: Evidence Binder Router — Assemble and export evidence binders for audit.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w09_evidence_binder import service

router = APIRouter(tags=["Evidence Binder"])

@router.get("/api/binders")
async def api_list(limit: int = 100):
    """List evidence binders"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/binders", status_code=201)
async def api_create(request: Request):
    """Create an evidence binder"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/binders/{binder_id}")
async def api_get(binder_id: str):
    """Get binder details"""
    item = service.get(binder_id)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder not found")
    return item

@router.post("/api/binders/{binder_id}/finalize")
async def api_finalize(binder_id: str, request: Request):
    """Finalize binder for export"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.finalize(binder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder not found")
    return item

@router.post("/api/binders/{binder_id}/sections")
async def api_add_section(binder_id: str, request: Request):
    """Add section to binder"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_section(binder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder not found")
    return item
