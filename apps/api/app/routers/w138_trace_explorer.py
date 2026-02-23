"""Wave 138: Trace Explorer Router — Observability and trace explorer hardening with searchable traces.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w138_trace_explorer import service

router = APIRouter(tags=["Trace Explorer"])

@router.get("/api/trace-explorer")
async def api_trace_explorer_w138_list_traces(limit: int = 100):
    """List traces"""
    items = service.list_traces(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/trace-explorer", status_code=201)
async def api_trace_explorer_w138_record_trace(request: Request):
    """Record trace span"""
    data = await request.json()
    item = service.record_trace(data)
    return item

@router.get("/api/trace-explorer/export")
async def api_trace_explorer_w138_export_traces(limit: int = 100):
    """Export trace data"""
    items = service.export_traces(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/trace-explorer/graph")
async def api_trace_explorer_w138_trace_graph(limit: int = 100):
    """Get trace dependency graph"""
    items = service.trace_graph(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/trace-explorer/{trace_id}")
async def api_trace_explorer_w138_get_trace(trace_id: str):
    """Get trace details"""
    item = service.get_trace(trace_id)
    if not item:
        raise HTTPException(status_code=404, detail="trace_explorer not found")
    return item

@router.post("/api/trace-explorer/{trace_id}/search")
async def api_trace_explorer_w138_search_traces(trace_id: str, request: Request):
    """Search related traces"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.search_traces(trace_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="trace_explorer not found")
    return item
