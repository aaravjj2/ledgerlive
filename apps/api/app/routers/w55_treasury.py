"""Wave 55: Treasury 2.0 Router — Debt schedules, interest projection, liquidity ladder view.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w55_treasury import service

router = APIRouter(tags=["Treasury 2.0"])

@router.get("/api/treasury/debt-schedule")
async def api_treasury_w55_debt_schedule(limit: int = 100):
    """Get debt maturity schedule"""
    items = service.debt_schedule(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/treasury/instruments")
async def api_treasury_w55_list_instruments(limit: int = 100):
    """List treasury instruments"""
    items = service.list_instruments(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/treasury/instruments", status_code=201)
async def api_treasury_w55_create_instrument(request: Request):
    """Create a treasury instrument"""
    data = await request.json()
    item = service.create_instrument(data)
    return item

@router.get("/api/treasury/liquidity-ladder")
async def api_treasury_w55_liquidity_ladder(limit: int = 100):
    """Get liquidity ladder view"""
    items = service.liquidity_ladder(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/treasury/instruments/{instrument_id}")
async def api_treasury_w55_get_instrument(instrument_id: str):
    """Get instrument details"""
    item = service.get_instrument(instrument_id)
    if not item:
        raise HTTPException(status_code=404, detail="treasury not found")
    return item

@router.post("/api/treasury/instruments/{instrument_id}/project")
async def api_treasury_w55_project_interest(instrument_id: str, request: Request):
    """Project interest"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.project_interest(instrument_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="treasury not found")
    return item
