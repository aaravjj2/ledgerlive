"""Wave 21: Report Generator Router — Financial close reports with configurable templates.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w21_report import service

router = APIRouter(tags=["Report Generator"])

@router.get("/api/reports")
async def api_list(limit: int = 100):
    """List reports"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/reports", status_code=201)
async def api_generate(request: Request):
    """Generate a report"""
    data = await request.json()
    item = service.generate(data)
    return item

@router.post("/api/reports/schedule", status_code=201)
async def api_schedule(request: Request):
    """Schedule recurring report"""
    data = await request.json()
    item = service.schedule(data)
    return item

@router.get("/api/reports/{report_id}")
async def api_get(report_id: str):
    """Get report details"""
    item = service.get(report_id)
    if not item:
        raise HTTPException(status_code=404, detail="report not found")
    return item

@router.get("/api/reports/{report_id}/preview")
async def api_preview(report_id: str):
    """Preview report"""
    item = service.preview(report_id)
    if not item:
        raise HTTPException(status_code=404, detail="report not found")
    return item
