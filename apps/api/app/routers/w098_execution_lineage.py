"""Wave 98: Execution Lineage Router — Lineage recording for workflow/template execution with provenance.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w098_execution_lineage import service

router = APIRouter(tags=["Execution Lineage"])

@router.get("/api/execution-lineage")
async def api_execution_lineage_w98_list_lineage(limit: int = 100):
    """List execution lineage records"""
    items = service.list_lineage(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/execution-lineage", status_code=201)
async def api_execution_lineage_w98_record_lineage(request: Request):
    """Record execution lineage"""
    data = await request.json()
    item = service.record_lineage(data)
    return item

@router.get("/api/execution-lineage/export")
async def api_execution_lineage_w98_export_lineage(limit: int = 100):
    """Export lineage records"""
    items = service.export_lineage(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/execution-lineage/graph")
async def api_execution_lineage_w98_lineage_graph(limit: int = 100):
    """Get lineage graph"""
    items = service.lineage_graph(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/execution-lineage/{lineage_id}")
async def api_execution_lineage_w98_get_lineage(lineage_id: str):
    """Get lineage details"""
    item = service.get_lineage(lineage_id)
    if not item:
        raise HTTPException(status_code=404, detail="execution_lineage not found")
    return item

@router.post("/api/execution-lineage/{lineage_id}/verify")
async def api_execution_lineage_w98_verify_lineage(lineage_id: str, request: Request):
    """Verify lineage integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_lineage(lineage_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="execution_lineage not found")
    return item
