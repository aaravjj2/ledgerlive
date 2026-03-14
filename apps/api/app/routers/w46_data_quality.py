"""Wave 46: Data Quality Engine Router — Data quality rules (missing fields, duplicates, outliers), quality scorecard per close.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w46_data_quality import service

router = APIRouter(tags=["Data Quality Engine"])

@router.get("/api/data-quality/checks")
async def api_data_quality_w46_list_checks(limit: int = 100):
    """List data quality checks"""
    items = service.list_checks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/data-quality/checks", status_code=201)
async def api_data_quality_w46_run_check(request: Request):
    """Run a data quality check"""
    data = await request.json()
    item = service.run_check(data)
    return item

@router.get("/api/data-quality/export")
async def api_data_quality_w46_export_report(limit: int = 100):
    """Export quality report"""
    items = service.export_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-quality/scorecard")
async def api_data_quality_w46_scorecard(limit: int = 100):
    """Get quality scorecard"""
    items = service.scorecard(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-quality/checks/{check_id}")
async def api_data_quality_w46_get_check(check_id: str):
    """Get check details"""
    item = service.get_check(check_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_quality not found")
    return item

@router.post("/api/data-quality/checks/{check_id}/approve")
async def api_data_quality_w46_approve_override(check_id: str, request: Request):
    """Approve quality override"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_override(check_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_quality not found")
    return item
