"""Wave 36: Accruals & Deferrals Router — Recurring schedules, accrual proposals from patterns, approval required, automatic reversals.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w36_accruals_deferrals import service

router = APIRouter(tags=["Accruals & Deferrals"])

@router.get("/api/accruals")
async def api_accruals_deferrals_w36_list_schedules(limit: int = 100):
    """List accrual/deferral schedules"""
    items = service.list_schedules(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/accruals", status_code=201)
async def api_accruals_deferrals_w36_create_schedule(request: Request):
    """Create an accrual/deferral schedule"""
    data = await request.json()
    item = service.create_schedule(data)
    return item

@router.get("/api/accruals/export")
async def api_accruals_deferrals_w36_export_accruals(limit: int = 100):
    """Export accrual report"""
    items = service.export_accruals(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/accruals/{schedule_id}")
async def api_accruals_deferrals_w36_get_schedule(schedule_id: str):
    """Get schedule details"""
    item = service.get_schedule(schedule_id)
    if not item:
        raise HTTPException(status_code=404, detail="accruals_deferrals not found")
    return item

@router.post("/api/accruals/{schedule_id}/approve")
async def api_accruals_deferrals_w36_approve_proposal(schedule_id: str, request: Request):
    """Approve accrual proposal"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_proposal(schedule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="accruals_deferrals not found")
    return item

@router.post("/api/accruals/{schedule_id}/propose")
async def api_accruals_deferrals_w36_generate_proposal(schedule_id: str, request: Request):
    """Generate accrual proposal"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_proposal(schedule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="accruals_deferrals not found")
    return item

@router.post("/api/accruals/{schedule_id}/reverse")
async def api_accruals_deferrals_w36_reverse(schedule_id: str, request: Request):
    """Reverse an accrual"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reverse(schedule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="accruals_deferrals not found")
    return item
