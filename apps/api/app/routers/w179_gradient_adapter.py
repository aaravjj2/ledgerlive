"""Wave 179: DigitalOcean Gradient Adapter Skeleton Router — Config and scripts for Gradient training/inference. DEMO uses local model artifacts. Deterministic would-run plan output.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w179_gradient_adapter import service

router = APIRouter(tags=["DigitalOcean Gradient Adapter Skeleton"])

@router.get("/api/gradient-adapter")
async def api_gradient_adapter_w179_list_plans(limit: int = 100):
    """List Gradient adapter plans"""
    items = service.list_plans(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gradient-adapter", status_code=201)
async def api_gradient_adapter_w179_create_plan(request: Request):
    """Create Gradient adapter plan"""
    data = await request.json()
    item = service.create_plan(data)
    return item

@router.get("/api/gradient-adapter/report")
async def api_gradient_adapter_w179_plan_report(limit: int = 100):
    """Get plan report"""
    items = service.plan_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gradient-adapter/{plan_id}")
async def api_gradient_adapter_w179_get_plan(plan_id: str):
    """Get plan details"""
    item = service.get_plan(plan_id)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_adapter not found")
    return item

@router.post("/api/gradient-adapter/{plan_id}/simulate")
async def api_gradient_adapter_w179_simulate_plan(plan_id: str, request: Request):
    """Simulate plan execution"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.simulate_plan(plan_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_adapter not found")
    return item

@router.post("/api/gradient-adapter/{plan_id}/validate")
async def api_gradient_adapter_w179_validate_plan(plan_id: str, request: Request):
    """Validate plan config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_plan(plan_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_adapter not found")
    return item
