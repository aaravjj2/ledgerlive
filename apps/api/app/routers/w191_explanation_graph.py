"""Wave 191: Explanation Graph v3 Router — Reason DAG linking exception to evidence to model outputs to policy decisions to approvals to final resolution. Every node must reference evidence IDs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w191_explanation_graph import service

router = APIRouter(tags=["Explanation Graph v3"])

@router.get("/api/explanation-graphs")
async def api_explanation_graph_w191_list_graphs(limit: int = 100):
    """List explanation graphs"""
    items = service.list_graphs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/explanation-graphs", status_code=201)
async def api_explanation_graph_w191_create_graph(request: Request):
    """Create explanation graph"""
    data = await request.json()
    item = service.create_graph(data)
    return item

@router.get("/api/explanation-graphs/report")
async def api_explanation_graph_w191_graph_report(limit: int = 100):
    """Get explanation graph report"""
    items = service.graph_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/explanation-graphs/{graph_id}")
async def api_explanation_graph_w191_get_graph(graph_id: str):
    """Get graph details"""
    item = service.get_graph(graph_id)
    if not item:
        raise HTTPException(status_code=404, detail="explanation_graph not found")
    return item

@router.post("/api/explanation-graphs/{graph_id}/node")
async def api_explanation_graph_w191_add_node(graph_id: str, request: Request):
    """Add node with citation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_node(graph_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="explanation_graph not found")
    return item

@router.post("/api/explanation-graphs/{graph_id}/serialize")
async def api_explanation_graph_w191_serialize_dag(graph_id: str, request: Request):
    """Serialize DAG deterministically"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.serialize_dag(graph_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="explanation_graph not found")
    return item

@router.post("/api/explanation-graphs/{graph_id}/validate")
async def api_explanation_graph_w191_validate_citations(graph_id: str, request: Request):
    """Validate all nodes have citations"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_citations(graph_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="explanation_graph not found")
    return item
