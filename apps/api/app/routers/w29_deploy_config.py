"""Wave 29: Deploy Configuration Router — GCP deployment configuration and environment management.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w29_deploy_config import service

router = APIRouter(tags=["Deploy Configuration"])

@router.get("/api/deploy/configs")
async def api_list(limit: int = 100):
    """List deploy configs"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/deploy/configs", status_code=201)
async def api_create(request: Request):
    """Create deploy config"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/deploy/configs/{config_id}")
async def api_get(config_id: str):
    """Get config details"""
    item = service.get(config_id)
    if not item:
        raise HTTPException(status_code=404, detail="deploy_config not found")
    return item

@router.post("/api/deploy/configs/{config_id}/activate")
async def api_activate(config_id: str, request: Request):
    """Activate config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.activate(config_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="deploy_config not found")
    return item

@router.post("/api/deploy/configs/{config_id}/validate")
async def api_validate_config(config_id: str, request: Request):
    """Validate config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_config(config_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="deploy_config not found")
    return item
