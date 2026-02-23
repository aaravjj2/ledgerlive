"""Wave 51: Budgeting 1.0 Router — Budget versions, approval routing, locking, variance hooks.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w51_budgeting import service

router = APIRouter(tags=["Budgeting 1.0"])

@router.get("/api/budgets")
async def api_budgeting_w51_list_budgets(limit: int = 100):
    """List budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/budgets", status_code=201)
async def api_budgeting_w51_create_budget(request: Request):
    """Create a budget"""
    data = await request.json()
    item = service.create_budget(data)
    return item

@router.get("/api/budgets/variance")
async def api_budgeting_w51_variance_report(limit: int = 100):
    """Get budget variance report"""
    items = service.variance_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/budgets/{budget_id}")
async def api_budgeting_w51_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="budgeting not found")
    return item

@router.post("/api/budgets/{budget_id}/approve")
async def api_budgeting_w51_approve_budget(budget_id: str, request: Request):
    """Approve a budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_budget(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="budgeting not found")
    return item

@router.post("/api/budgets/{budget_id}/lock")
async def api_budgeting_w51_lock_budget(budget_id: str, request: Request):
    """Lock a budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.lock_budget(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="budgeting not found")
    return item

@router.post("/api/budgets/{budget_id}/publish")
async def api_budgeting_w51_publish_budget(budget_id: str, request: Request):
    """Publish a budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.publish_budget(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="budgeting not found")
    return item

@router.post("/api/budgets/{budget_id}/submit")
async def api_budgeting_w51_submit_budget(budget_id: str, request: Request):
    """Submit budget for approval"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.submit_budget(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="budgeting not found")
    return item
