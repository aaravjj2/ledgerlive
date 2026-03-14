"""Wave 301: Blueprint Builder v1 Router — Visual step list editor with approvals/policies per step and deterministic export.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w301_blueprint_builder_v1 import service

router = APIRouter(tags=["Blueprint Builder v1"])

@router.get("/api/blueprint-builder")
async def api_blueprint_builder_v1_w301_list_blueprints(limit: int = 100):
    """List blueprints"""
    items = service.list_blueprints(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/blueprint-builder", status_code=201)
async def api_blueprint_builder_v1_w301_create_blueprint(request: Request):
    """Create blueprint"""
    data = await request.json()
    item = service.create_blueprint(data)
    return item

@router.get("/api/blueprint-builder/report")
async def api_blueprint_builder_v1_w301_blueprint_report(limit: int = 100):
    """Get blueprint builder report"""
    items = service.blueprint_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/blueprint-builder/{blueprint_id}")
async def api_blueprint_builder_v1_w301_get_blueprint(blueprint_id: str):
    """Get blueprint details"""
    item = service.get_blueprint(blueprint_id)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v1 not found")
    return item

@router.post("/api/blueprint-builder/{blueprint_id}/add-step")
async def api_blueprint_builder_v1_w301_add_step(blueprint_id: str, request: Request):
    """Add step to blueprint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_step(blueprint_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v1 not found")
    return item

@router.post("/api/blueprint-builder/{blueprint_id}/export")
async def api_blueprint_builder_v1_w301_export_blueprint(blueprint_id: str, request: Request):
    """Export blueprint deterministically"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_blueprint(blueprint_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v1 not found")
    return item

@router.post("/api/blueprint-builder/{blueprint_id}/policy")
async def api_blueprint_builder_v1_w301_set_policy(blueprint_id: str, request: Request):
    """Set approval policy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_policy(blueprint_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_builder_v1 not found")
    return item
