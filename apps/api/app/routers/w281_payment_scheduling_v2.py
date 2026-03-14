"""Wave 281: Payment Scheduling v2 Router — Cash-aware approval gates with vendor risk integration and treasury ladder support. Deterministic scheduling with conflict detection.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w281_payment_scheduling_v2 import service

router = APIRouter(tags=["Payment Scheduling v2"])

@router.get("/api/payment-scheduling-v2")
async def api_payment_scheduling_v2_w281_list_schedules(limit: int = 100):
    """List payment schedules"""
    items = service.list_schedules(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/payment-scheduling-v2", status_code=201)
async def api_payment_scheduling_v2_w281_create_schedule(request: Request):
    """Create payment schedule"""
    data = await request.json()
    item = service.create_schedule(data)
    return item

@router.get("/api/payment-scheduling-v2/report")
async def api_payment_scheduling_v2_w281_schedule_report(limit: int = 100):
    """Get payment scheduling report"""
    items = service.schedule_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/payment-scheduling-v2/{schedule_id}")
async def api_payment_scheduling_v2_w281_get_schedule(schedule_id: str):
    """Get schedule details"""
    item = service.get_schedule(schedule_id)
    if not item:
        raise HTTPException(status_code=404, detail="payment_scheduling_v2 not found")
    return item

@router.post("/api/payment-scheduling-v2/{schedule_id}/approve")
async def api_payment_scheduling_v2_w281_approve_payment(schedule_id: str, request: Request):
    """Approve payment"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_payment(schedule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="payment_scheduling_v2 not found")
    return item

@router.post("/api/payment-scheduling-v2/{schedule_id}/cash-check")
async def api_payment_scheduling_v2_w281_check_cash(schedule_id: str, request: Request):
    """Check cash availability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_cash(schedule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="payment_scheduling_v2 not found")
    return item

@router.post("/api/payment-scheduling-v2/{schedule_id}/vendor-risk")
async def api_payment_scheduling_v2_w281_assess_vendor_risk(schedule_id: str, request: Request):
    """Assess vendor risk"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assess_vendor_risk(schedule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="payment_scheduling_v2 not found")
    return item
