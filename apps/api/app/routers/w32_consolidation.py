"""Wave 32: Multi-Entity Consolidation Router — Entity hierarchy, consolidation adjustments, intercompany eliminations, consolidated P&L/BS.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w32_consolidation import service

router = APIRouter(tags=["Multi-Entity Consolidation"])

@router.get("/api/consolidations")
async def api_consolidation_w32_list(limit: int = 100):
    """List consolidation runs"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/consolidations", status_code=201)
async def api_consolidation_w32_create(request: Request):
    """Start a consolidation run"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/consolidations/export")
async def api_consolidation_w32_export_statements(limit: int = 100):
    """Export consolidated statements"""
    items = service.export_statements(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/consolidations/{consolidation_id}")
async def api_consolidation_w32_get(consolidation_id: str):
    """Get consolidation details"""
    item = service.get(consolidation_id)
    if not item:
        raise HTTPException(status_code=404, detail="consolidation not found")
    return item

@router.post("/api/consolidations/{consolidation_id}/adjustments")
async def api_consolidation_w32_add_adjustment(consolidation_id: str, request: Request):
    """Add consolidation adjustment"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_adjustment(consolidation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consolidation not found")
    return item

@router.post("/api/consolidations/{consolidation_id}/eliminations")
async def api_consolidation_w32_add_elimination(consolidation_id: str, request: Request):
    """Add intercompany elimination"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_elimination(consolidation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consolidation not found")
    return item

@router.post("/api/consolidations/{consolidation_id}/finalize")
async def api_consolidation_w32_finalize(consolidation_id: str, request: Request):
    """Finalize consolidation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.finalize(consolidation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consolidation not found")
    return item
