"""Wave 113: Evidence Query Language 2.0 Router — Query language for evidence and audit data with saved queries.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w113_query_language import service

router = APIRouter(tags=["Evidence Query Language 2.0"])

@router.get("/api/evidence-queries")
async def api_query_language_w113_list_queries(limit: int = 100):
    """List saved queries"""
    items = service.list_queries(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/evidence-queries", status_code=201)
async def api_query_language_w113_execute_query(request: Request):
    """Execute evidence query"""
    data = await request.json()
    item = service.execute_query(data)
    return item

@router.get("/api/evidence-queries/export")
async def api_query_language_w113_export_results(limit: int = 100):
    """Export query results"""
    items = service.export_results(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/evidence-queries/history")
async def api_query_language_w113_query_history(limit: int = 100):
    """Get query execution history"""
    items = service.query_history(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/evidence-queries/{query_id}")
async def api_query_language_w113_get_query(query_id: str):
    """Get query details"""
    item = service.get_query(query_id)
    if not item:
        raise HTTPException(status_code=404, detail="query_language not found")
    return item

@router.post("/api/evidence-queries/{query_id}/save")
async def api_query_language_w113_save_query(query_id: str, request: Request):
    """Save query"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.save_query(query_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="query_language not found")
    return item
