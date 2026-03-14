"""Wave 40: Evidence Binder 2.0 Router — Audit-ready binder with controls report, approvals chain, provenance, Merkle integrity, signing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w40_evidence_binder_v2 import service

router = APIRouter(tags=["Evidence Binder 2.0"])

@router.get("/api/binders-v2")
async def api_evidence_binder_v2_w40_list_binders(limit: int = 100):
    """List evidence binders v2"""
    items = service.list_binders(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/binders-v2", status_code=201)
async def api_evidence_binder_v2_w40_create_binder(request: Request):
    """Create evidence binder v2"""
    data = await request.json()
    item = service.create_binder(data)
    return item

@router.get("/api/binders-v2/export")
async def api_evidence_binder_v2_w40_export_binder(limit: int = 100):
    """Export audit-ready binder"""
    items = service.export_binder(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/binders-v2/{binder_id}")
async def api_evidence_binder_v2_w40_get_binder(binder_id: str):
    """Get binder details"""
    item = service.get_binder(binder_id)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder_v2 not found")
    return item

@router.post("/api/binders-v2/{binder_id}/provenance")
async def api_evidence_binder_v2_w40_add_provenance(binder_id: str, request: Request):
    """Add provenance record"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_provenance(binder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder_v2 not found")
    return item

@router.post("/api/binders-v2/{binder_id}/sign")
async def api_evidence_binder_v2_w40_sign_binder(binder_id: str, request: Request):
    """Sign the binder"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_binder(binder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder_v2 not found")
    return item

@router.post("/api/binders-v2/{binder_id}/verify")
async def api_evidence_binder_v2_w40_verify_binder(binder_id: str, request: Request):
    """Verify binder integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_binder(binder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="evidence_binder_v2 not found")
    return item
