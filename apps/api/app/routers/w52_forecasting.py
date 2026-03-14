"""Wave 52: Forecasting 1.0 Router — Baseline forecasting (moving average, seasonal naive), model registry, drift alerts.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w52_forecasting import service

router = APIRouter(tags=["Forecasting 1.0"])

@router.get("/api/forecasts")
async def api_forecasting_w52_list_forecasts(limit: int = 100):
    """List forecasts"""
    items = service.list_forecasts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/forecasts", status_code=201)
async def api_forecasting_w52_create_forecast(request: Request):
    """Create a forecast"""
    data = await request.json()
    item = service.create_forecast(data)
    return item

@router.get("/api/forecasts/registry")
async def api_forecasting_w52_model_registry(limit: int = 100):
    """Get model registry"""
    items = service.model_registry(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/forecasts/{forecast_id}")
async def api_forecasting_w52_get_forecast(forecast_id: str):
    """Get forecast details"""
    item = service.get_forecast(forecast_id)
    if not item:
        raise HTTPException(status_code=404, detail="forecasting not found")
    return item

@router.post("/api/forecasts/{forecast_id}/drift")
async def api_forecasting_w52_detect_drift(forecast_id: str, request: Request):
    """Run drift detection"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.detect_drift(forecast_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="forecasting not found")
    return item

@router.post("/api/forecasts/{forecast_id}/evaluate")
async def api_forecasting_w52_evaluate(forecast_id: str, request: Request):
    """Evaluate forecast accuracy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate(forecast_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="forecasting not found")
    return item

@router.post("/api/forecasts/{forecast_id}/register")
async def api_forecasting_w52_register_model(forecast_id: str, request: Request):
    """Register model in registry"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.register_model(forecast_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="forecasting not found")
    return item
