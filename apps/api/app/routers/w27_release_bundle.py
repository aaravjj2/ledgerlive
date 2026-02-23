"""Wave 27: Release Bundle Router — Versioned release bundles with changelog and migration tracking.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w27_release_bundle import service

router = APIRouter(tags=["Release Bundle"])

@router.get("/api/releases")
async def api_list(limit: int = 100):
    """List releases"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/releases", status_code=201)
async def api_create(request: Request):
    """Create a release bundle"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/releases/{release_id}")
async def api_get(release_id: str):
    """Get release details"""
    item = service.get(release_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle not found")
    return item

@router.post("/api/releases/{release_id}/deploy")
async def api_deploy(release_id: str, request: Request):
    """Mark as deployed"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deploy(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle not found")
    return item

@router.post("/api/releases/{release_id}/rollback")
async def api_rollback(release_id: str, request: Request):
    """Rollback a release"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle not found")
    return item
