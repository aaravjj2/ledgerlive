"""Wave 302: Blueprint Builder v2 Router — Step dependency graph editing with validation and critical path preview.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w302_blueprint_builder_v2 import service

router = APIRouter(tags=["Blueprint Builder v2"])

@router.get("/api/blueprint-graph")
async def api_blueprint_builder_v2_w302_list_graphs(limit: int = 100):
    """List dependency graphs"""
    items = service.list_graphs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/blueprint-graph", status_code=201)
async def api_blueprint_builder_v2_w302_create_graph(request: Request):
    """Create dependency graph"""
    data = await request.json()
    item = service.create_graph(data)
    return item

@router.get("/api/blueprint-graph/report")
async def api_blueprint_builder_v2_w302_graph_report(limit: int = 100):
    """Get graph report"""
    items = service.graph_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/blueprint-graph/{graph_id}")
async def api_blueprint_builder_v2_w302_get_graph(graph_id: str):
    """Get graph details"""
    item = service.get_graph(graph_id)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v2 not found")
    return item

@router.post("/api/blueprint-graph/{graph_id}/critical-path")
async def api_blueprint_builder_v2_w302_critical_path(graph_id: str, request: Request):
    """Preview critical path"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.critical_path(graph_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v2 not found")
    return item

@router.post("/api/blueprint-graph/{graph_id}/validate")
async def api_blueprint_builder_v2_w302_validate_graph(graph_id: str, request: Request):
    """Validate dependency graph"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_graph(graph_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v2 not found")
    return item
