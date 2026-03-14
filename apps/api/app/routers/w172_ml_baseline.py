"""Wave 172: ML Baseline Models v1 Router — Deterministic baseline models: extraction confidence calibration and match likelihood scoring. Seeded training with stable artifact hashes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w172_ml_baseline import service

router = APIRouter(tags=["ML Baseline Models v1"])

@router.get("/api/ml-baseline")
async def api_ml_baseline_w172_list_models(limit: int = 100):
    """List baseline models"""
    items = service.list_models(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ml-baseline", status_code=201)
async def api_ml_baseline_w172_train_model(request: Request):
    """Train baseline model"""
    data = await request.json()
    item = service.train_model(data)
    return item

@router.get("/api/ml-baseline/report")
async def api_ml_baseline_w172_model_report(limit: int = 100):
    """Get model training report"""
    items = service.model_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ml-baseline/{model_id}")
async def api_ml_baseline_w172_get_model(model_id: str):
    """Get model details"""
    item = service.get_model(model_id)
    if not item:
        raise HTTPException(status_code=404, detail="ml_baseline not found")
    return item

@router.post("/api/ml-baseline/{model_id}/evaluate")
async def api_ml_baseline_w172_evaluate_model(model_id: str, request: Request):
    """Evaluate model metrics"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_model(model_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_baseline not found")
    return item

@router.post("/api/ml-baseline/{model_id}/register")
async def api_ml_baseline_w172_register_model(model_id: str, request: Request):
    """Register model artifact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.register_model(model_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_baseline not found")
    return item
