"""Wave 22: Search Index Router — Full-text search across documents, extractions, and audit events.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w22_search_index import service

router = APIRouter(tags=["Search Index"])

@router.get("/api/search")
async def api_search(limit: int = 100):
    """Execute full-text search"""
    items = service.search(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/search/facets")
async def api_facets(limit: int = 100):
    """Get search facets"""
    items = service.facets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/search/reindex", status_code=201)
async def api_reindex(request: Request):
    """Trigger reindexing"""
    data = await request.json()
    item = service.reindex(data)
    return item

@router.get("/api/search/stats")
async def api_stats(limit: int = 100):
    """Search index statistics"""
    items = service.stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/search/suggest")
async def api_suggest(limit: int = 100):
    """Auto-complete suggestions"""
    items = service.suggest(limit=limit)
    return {"items": items, "total": len(items)}
