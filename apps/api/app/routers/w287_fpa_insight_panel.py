"""Wave 287: FP&A Insight Panel v1 Router — Budgets, forecast, and scenario deltas surfaced in Race Control as telemetry. Deterministic variance analysis.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w287_fpa_insight_panel import service

router = APIRouter(tags=["FP&A Insight Panel v1"])

@router.get("/api/fpa-insight-panel")
async def api_fpa_insight_panel_w287_list_insights(limit: int = 100):
    """List FP&A insights"""
    items = service.list_insights(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/fpa-insight-panel", status_code=201)
async def api_fpa_insight_panel_w287_create_insight(request: Request):
    """Create FP&A insight"""
    data = await request.json()
    item = service.create_insight(data)
    return item

@router.get("/api/fpa-insight-panel/report")
async def api_fpa_insight_panel_w287_insight_report(limit: int = 100):
    """Get FP&A insight report"""
    items = service.insight_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/fpa-insight-panel/{insight_id}")
async def api_fpa_insight_panel_w287_get_insight(insight_id: str):
    """Get insight details"""
    item = service.get_insight(insight_id)
    if not item:
        raise HTTPException(status_code=404, detail="fpa_insight_panel not found")
    return item

@router.post("/api/fpa-insight-panel/{insight_id}/scenario")
async def api_fpa_insight_panel_w287_run_scenario(insight_id: str, request: Request):
    """Run scenario analysis"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_scenario(insight_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fpa_insight_panel not found")
    return item

@router.post("/api/fpa-insight-panel/{insight_id}/variance")
async def api_fpa_insight_panel_w287_analyze_variance(insight_id: str, request: Request):
    """Analyze variance"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.analyze_variance(insight_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fpa_insight_panel not found")
    return item
