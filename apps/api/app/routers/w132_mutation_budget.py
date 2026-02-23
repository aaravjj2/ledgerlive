"""Wave 132: Mutation Testing Budget Router — Mutation testing budgets and guards preventing quality regression.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w132_mutation_budget import service

router = APIRouter(tags=["Mutation Testing Budget"])

@router.get("/api/mutation-budgets")
async def api_mutation_budget_w132_list_budgets(limit: int = 100):
    """List mutation testing budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/mutation-budgets", status_code=201)
async def api_mutation_budget_w132_set_budget(request: Request):
    """Set mutation budget"""
    data = await request.json()
    item = service.set_budget(data)
    return item

@router.get("/api/mutation-budgets/report")
async def api_mutation_budget_w132_budget_report(limit: int = 100):
    """Get mutation budget report"""
    items = service.budget_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/mutation-budgets/{budget_id}")
async def api_mutation_budget_w132_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="mutation_budget not found")
    return item

@router.post("/api/mutation-budgets/{budget_id}/measure")
async def api_mutation_budget_w132_measure(budget_id: str, request: Request):
    """Measure mutation kill rate"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="mutation_budget not found")
    return item
