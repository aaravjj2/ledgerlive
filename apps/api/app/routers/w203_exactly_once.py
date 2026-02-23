"""Wave 203: Exactly-Once Tool Effects v2 Router — Every tool call requires idempotency_key. Executor enforces exactly-once. Side effect ledger per close_period for verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w203_exactly_once import service

router = APIRouter(tags=["Exactly-Once Tool Effects v2"])

@router.get("/api/exactly-once")
async def api_exactly_once_w203_list_effects(limit: int = 100):
    """List tool effect records"""
    items = service.list_effects(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/exactly-once", status_code=201)
async def api_exactly_once_w203_record_effect(request: Request):
    """Record tool effect with idempotency key"""
    data = await request.json()
    item = service.record_effect(data)
    return item

@router.get("/api/exactly-once/report")
async def api_exactly_once_w203_effect_report(limit: int = 100):
    """Get exactly-once report"""
    items = service.effect_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/exactly-once/{effect_id}")
async def api_exactly_once_w203_get_effect(effect_id: str):
    """Get effect details"""
    item = service.get_effect(effect_id)
    if not item:
        raise HTTPException(status_code=404, detail="exactly_once not found")
    return item

@router.post("/api/exactly-once/{effect_id}/hammer")
async def api_exactly_once_w203_hammer_test(effect_id: str, request: Request):
    """Hammer test same key multiple times"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.hammer_test(effect_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exactly_once not found")
    return item

@router.post("/api/exactly-once/{effect_id}/verify")
async def api_exactly_once_w203_verify_once(effect_id: str, request: Request):
    """Verify exactly-once enforcement"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_once(effect_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exactly_once not found")
    return item
