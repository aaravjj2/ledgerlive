"""Wave 323: Readiness Dashboard v1 Router — Single screen showing publish readiness checklist status (offline deterministic).

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w323_readiness_dashboard import service

router = APIRouter(tags=["Readiness Dashboard v1"])

@router.get("/api/readiness-dashboard")
async def api_readiness_dashboard_w323_list_dashboards(limit: int = 100):
    """List readiness dashboards"""
    items = service.list_dashboards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/readiness-dashboard", status_code=201)
async def api_readiness_dashboard_w323_create_dashboard(request: Request):
    """Create readiness dashboard"""
    data = await request.json()
    item = service.create_dashboard(data)
    return item

@router.get("/api/readiness-dashboard/report")
async def api_readiness_dashboard_w323_dashboard_report(limit: int = 100):
    """Get readiness dashboard report"""
    items = service.dashboard_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/readiness-dashboard/{dashboard_id}")
async def api_readiness_dashboard_w323_get_dashboard(dashboard_id: str):
    """Get dashboard details"""
    item = service.get_dashboard(dashboard_id)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_dashboard not found")
    return item

@router.post("/api/readiness-dashboard/{dashboard_id}/check")
async def api_readiness_dashboard_w323_run_checklist(dashboard_id: str, request: Request):
    """Run readiness checklist"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_checklist(dashboard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_dashboard not found")
    return item

@router.post("/api/readiness-dashboard/{dashboard_id}/export")
async def api_readiness_dashboard_w323_export_status(dashboard_id: str, request: Request):
    """Export readiness status"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_status(dashboard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_dashboard not found")
    return item
