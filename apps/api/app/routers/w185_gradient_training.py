"""Wave 185: Gradient Training Spec v1 Router — DigitalOcean Gradient training job spec templates, inference deployment specs, config schema, validator. Deterministic plan output with hashes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w185_gradient_training import service

router = APIRouter(tags=["Gradient Training Spec v1"])

@router.get("/api/gradient-training")
async def api_gradient_training_w185_list_specs(limit: int = 100):
    """List Gradient training specs"""
    items = service.list_specs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gradient-training", status_code=201)
async def api_gradient_training_w185_create_spec(request: Request):
    """Create Gradient training spec"""
    data = await request.json()
    item = service.create_spec(data)
    return item

@router.get("/api/gradient-training/report")
async def api_gradient_training_w185_spec_report(limit: int = 100):
    """Get training spec report"""
    items = service.spec_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gradient-training/{spec_id}")
async def api_gradient_training_w185_get_spec(spec_id: str):
    """Get spec details"""
    item = service.get_spec(spec_id)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_training not found")
    return item

@router.post("/api/gradient-training/{spec_id}/render")
async def api_gradient_training_w185_render_plan(spec_id: str, request: Request):
    """Render deterministic would-run plan"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.render_plan(spec_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_training not found")
    return item

@router.post("/api/gradient-training/{spec_id}/validate")
async def api_gradient_training_w185_validate_spec(spec_id: str, request: Request):
    """Validate spec config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_spec(spec_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_training not found")
    return item
