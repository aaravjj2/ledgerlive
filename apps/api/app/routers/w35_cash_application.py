"""Wave 35: Cash Application Router — AR allocations, partial payments, deduction/dispute workflow.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w35_cash_application import service

router = APIRouter(tags=["Cash Application"])

@router.get("/api/cash-applications")
async def api_cash_application_w35_list(limit: int = 100):
    """List cash applications"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/cash-applications", status_code=201)
async def api_cash_application_w35_apply(request: Request):
    """Apply cash to invoice"""
    data = await request.json()
    item = service.apply(data)
    return item

@router.get("/api/cash-applications/export")
async def api_cash_application_w35_export_ar(limit: int = 100):
    """Export AR aging report"""
    items = service.export_ar(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cash-applications/{application_id}")
async def api_cash_application_w35_get(application_id: str):
    """Get application details"""
    item = service.get(application_id)
    if not item:
        raise HTTPException(status_code=404, detail="cash_application not found")
    return item

@router.post("/api/cash-applications/{application_id}/dispute")
async def api_cash_application_w35_dispute(application_id: str, request: Request):
    """Open a dispute"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.dispute(application_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cash_application not found")
    return item

@router.post("/api/cash-applications/{application_id}/resolve")
async def api_cash_application_w35_resolve_dispute(application_id: str, request: Request):
    """Resolve a dispute"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve_dispute(application_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cash_application not found")
    return item
