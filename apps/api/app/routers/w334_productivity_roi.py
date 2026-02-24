"""Wave 334: Productivity ROI Estimator v1 Router — Time saved, exceptions prevented, SLA compliance; deterministic calculation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w334_productivity_roi import service

router = APIRouter(tags=["Productivity ROI Estimator v1"])

@router.get("/api/productivity-roi")
async def api_productivity_roi_w334_list_rois(limit: int = 100):
    """List ROI estimates"""
    items = service.list_rois(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/productivity-roi", status_code=201)
async def api_productivity_roi_w334_calculate_roi(request: Request):
    """Calculate ROI"""
    data = await request.json()
    item = service.calculate_roi(data)
    return item

@router.get("/api/productivity-roi/report")
async def api_productivity_roi_w334_roi_report(limit: int = 100):
    """Get productivity ROI report"""
    items = service.roi_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/productivity-roi/{roi_id}")
async def api_productivity_roi_w334_get_roi(roi_id: str):
    """Get ROI details"""
    item = service.get_roi(roi_id)
    if not item:
        raise HTTPException(status_code=404, detail="productivity_roi not found")
    return item

@router.post("/api/productivity-roi/{roi_id}/export")
async def api_productivity_roi_w334_export_report(roi_id: str, request: Request):
    """Export ROI report"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_report(roi_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="productivity_roi not found")
    return item

@router.post("/api/productivity-roi/{roi_id}/recalculate")
async def api_productivity_roi_w334_recalculate(roi_id: str, request: Request):
    """Recalculate ROI"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recalculate(roi_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="productivity_roi not found")
    return item
