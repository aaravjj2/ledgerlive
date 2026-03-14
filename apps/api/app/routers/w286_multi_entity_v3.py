"""Wave 286: Multi-Entity Consolidation v3 Router — Deeper eliminations, FX, and CTA with statement notes and evidence links. Deterministic consolidation calculations.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w286_multi_entity_v3 import service

router = APIRouter(tags=["Multi-Entity Consolidation v3"])

@router.get("/api/multi-entity-v3")
async def api_multi_entity_v3_w286_list_consols(limit: int = 100):
    """List consolidations"""
    items = service.list_consols(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/multi-entity-v3", status_code=201)
async def api_multi_entity_v3_w286_create_consol(request: Request):
    """Create consolidation"""
    data = await request.json()
    item = service.create_consol(data)
    return item

@router.get("/api/multi-entity-v3/report")
async def api_multi_entity_v3_w286_consol_report(limit: int = 100):
    """Get consolidation report"""
    items = service.consol_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/multi-entity-v3/{consol_id}")
async def api_multi_entity_v3_w286_get_consol(consol_id: str):
    """Get consolidation details"""
    item = service.get_consol(consol_id)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_v3 not found")
    return item

@router.post("/api/multi-entity-v3/{consol_id}/eliminate")
async def api_multi_entity_v3_w286_apply_eliminations(consol_id: str, request: Request):
    """Apply elimination entries"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_eliminations(consol_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_v3 not found")
    return item

@router.post("/api/multi-entity-v3/{consol_id}/fx")
async def api_multi_entity_v3_w286_apply_fx(consol_id: str, request: Request):
    """Apply FX adjustments"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_fx(consol_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_v3 not found")
    return item

@router.post("/api/multi-entity-v3/{consol_id}/notes")
async def api_multi_entity_v3_w286_add_notes(consol_id: str, request: Request):
    """Add statement notes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_notes(consol_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_entity_v3 not found")
    return item
