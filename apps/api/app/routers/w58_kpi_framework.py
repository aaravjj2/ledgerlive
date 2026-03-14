"""Wave 58: KPI Framework Router — KPIs as objects with formulas + evidence links. No floating KPIs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w58_kpi_framework import service

router = APIRouter(tags=["KPI Framework"])

@router.get("/api/kpis")
async def api_kpi_framework_w58_list_kpis(limit: int = 100):
    """List KPIs"""
    items = service.list_kpis(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/kpis", status_code=201)
async def api_kpi_framework_w58_create_kpi(request: Request):
    """Create a KPI"""
    data = await request.json()
    item = service.create_kpi(data)
    return item

@router.get("/api/kpis/completeness")
async def api_kpi_framework_w58_completeness(limit: int = 100):
    """Check KPI completeness"""
    items = service.completeness(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/kpis/export")
async def api_kpi_framework_w58_export_kpis(limit: int = 100):
    """Export KPI report"""
    items = service.export_kpis(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/kpis/{kpi_id}")
async def api_kpi_framework_w58_get_kpi(kpi_id: str):
    """Get KPI details"""
    item = service.get_kpi(kpi_id)
    if not item:
        raise HTTPException(status_code=404, detail="kpi_framework not found")
    return item

@router.post("/api/kpis/{kpi_id}/compute")
async def api_kpi_framework_w58_compute(kpi_id: str, request: Request):
    """Compute KPI value"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compute(kpi_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="kpi_framework not found")
    return item

@router.post("/api/kpis/{kpi_id}/evidence")
async def api_kpi_framework_w58_link_evidence(kpi_id: str, request: Request):
    """Link evidence to KPI"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_evidence(kpi_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="kpi_framework not found")
    return item
