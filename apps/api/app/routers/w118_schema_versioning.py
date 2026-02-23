"""Wave 118: Schema Versioning Router — Deterministic schema version releases with migration tracking.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w118_schema_versioning import service

router = APIRouter(tags=["Schema Versioning"])

@router.get("/api/schema-versions")
async def api_schema_versioning_w118_list_schemas(limit: int = 100):
    """List schema versions"""
    items = service.list_schemas(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/schema-versions", status_code=201)
async def api_schema_versioning_w118_release_schema(request: Request):
    """Release schema version"""
    data = await request.json()
    item = service.release_schema(data)
    return item

@router.get("/api/schema-versions/history")
async def api_schema_versioning_w118_schema_history(limit: int = 100):
    """Get schema version history"""
    items = service.schema_history(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/schema-versions/{schema_id}")
async def api_schema_versioning_w118_get_schema(schema_id: str):
    """Get schema details"""
    item = service.get_schema(schema_id)
    if not item:
        raise HTTPException(status_code=404, detail="schema_versioning not found")
    return item

@router.post("/api/schema-versions/{schema_id}/apply")
async def api_schema_versioning_w118_apply_migration(schema_id: str, request: Request):
    """Apply migration"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_migration(schema_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="schema_versioning not found")
    return item

@router.post("/api/schema-versions/{schema_id}/rollback")
async def api_schema_versioning_w118_rollback_schema(schema_id: str, request: Request):
    """Rollback schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback_schema(schema_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="schema_versioning not found")
    return item
