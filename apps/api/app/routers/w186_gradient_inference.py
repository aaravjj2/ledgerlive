"""Wave 186: Gradient Inference Adapter v1 Router — Inference adapter behind ENABLE_GRADIENT_INFERENCE flag. DEMO uses local frozen artifacts. Safe fallback if live unavailable. Deterministic routing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w186_gradient_inference import service

router = APIRouter(tags=["Gradient Inference Adapter v1"])

@router.get("/api/gradient-inference")
async def api_gradient_inference_w186_list_adapters(limit: int = 100):
    """List inference adapter configs"""
    items = service.list_adapters(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gradient-inference", status_code=201)
async def api_gradient_inference_w186_create_adapter(request: Request):
    """Create inference adapter config"""
    data = await request.json()
    item = service.create_adapter(data)
    return item

@router.get("/api/gradient-inference/report")
async def api_gradient_inference_w186_adapter_report(limit: int = 100):
    """Get adapter report"""
    items = service.adapter_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gradient-inference/{adapter_id}")
async def api_gradient_inference_w186_get_adapter(adapter_id: str):
    """Get adapter details"""
    item = service.get_adapter(adapter_id)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_inference not found")
    return item

@router.post("/api/gradient-inference/{adapter_id}/fallback")
async def api_gradient_inference_w186_check_fallback(adapter_id: str, request: Request):
    """Check fallback behavior"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_fallback(adapter_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_inference not found")
    return item

@router.post("/api/gradient-inference/{adapter_id}/infer")
async def api_gradient_inference_w186_run_inference(adapter_id: str, request: Request):
    """Run inference with fallback"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_inference(adapter_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_inference not found")
    return item

@router.post("/api/gradient-inference/{adapter_id}/validate")
async def api_gradient_inference_w186_validate_adapter(adapter_id: str, request: Request):
    """Validate adapter config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_adapter(adapter_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_inference not found")
    return item
