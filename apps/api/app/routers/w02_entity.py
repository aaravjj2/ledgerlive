"""Wave 2: Entity Management Router — Legal entities / business units for multi-entity close.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w02_entity import service

router = APIRouter(tags=["Entity Management"])

@router.get("/api/entities")
async def api_list(limit: int = 100):
    """List all entities"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/entities", status_code=201)
async def api_create(request: Request):
    """Create an entity"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/entities/{entity_id}")
async def api_get(entity_id: str):
    """Get entity by ID"""
    item = service.get(entity_id)
    if not item:
        raise HTTPException(status_code=404, detail="entity not found")
    return item

@router.put("/api/entities/{entity_id}")
async def api_update(entity_id: str, request: Request):
    """Update entity"""
    data = await request.json()
    item = service.update(entity_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="entity not found")
    return item

@router.post("/api/entities/{entity_id}/deactivate")
async def api_deactivate(entity_id: str, request: Request):
    """Deactivate entity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deactivate(entity_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="entity not found")
    return item
