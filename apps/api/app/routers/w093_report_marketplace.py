"""Wave 93: Report Template Marketplace Router — Report templates with byte-equality renders and signature verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w093_report_marketplace import service

router = APIRouter(tags=["Report Template Marketplace"])

@router.get("/api/report-marketplace")
async def api_report_marketplace_w93_list_reports(limit: int = 100):
    """List report templates"""
    items = service.list_reports(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/report-marketplace", status_code=201)
async def api_report_marketplace_w93_publish(request: Request):
    """Publish report template"""
    data = await request.json()
    item = service.publish(data)
    return item

@router.get("/api/report-marketplace/export")
async def api_report_marketplace_w93_export_reports(limit: int = 100):
    """Export report templates"""
    items = service.export_reports(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/report-marketplace/{report_id}")
async def api_report_marketplace_w93_get_report(report_id: str):
    """Get report details"""
    item = service.get_report(report_id)
    if not item:
        raise HTTPException(status_code=404, detail="report_marketplace not found")
    return item

@router.post("/api/report-marketplace/{report_id}/import")
async def api_report_marketplace_w93_import_report(report_id: str, request: Request):
    """Import report template"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.import_report(report_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="report_marketplace not found")
    return item

@router.post("/api/report-marketplace/{report_id}/render")
async def api_report_marketplace_w93_render(report_id: str, request: Request):
    """Render report template"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.render(report_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="report_marketplace not found")
    return item

@router.post("/api/report-marketplace/{report_id}/verify")
async def api_report_marketplace_w93_verify_render(report_id: str, request: Request):
    """Verify render equality"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_render(report_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="report_marketplace not found")
    return item
