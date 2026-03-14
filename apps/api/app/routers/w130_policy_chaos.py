"""Wave 130: Policy Chaos Tests Router — Determinism and chaos tests for policy enforcement.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w130_policy_chaos import service

router = APIRouter(tags=["Policy Chaos Tests"])

@router.get("/api/policy-chaos")
async def api_policy_chaos_w130_list_chaos(limit: int = 100):
    """List policy chaos tests"""
    items = service.list_chaos(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/policy-chaos", status_code=201)
async def api_policy_chaos_w130_run_chaos(request: Request):
    """Run policy chaos test"""
    data = await request.json()
    item = service.run_chaos(data)
    return item

@router.get("/api/policy-chaos/report")
async def api_policy_chaos_w130_chaos_report(limit: int = 100):
    """Get policy chaos report"""
    items = service.chaos_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/policy-chaos/{chaos_id}")
async def api_policy_chaos_w130_get_chaos(chaos_id: str):
    """Get chaos test details"""
    item = service.get_chaos(chaos_id)
    if not item:
        raise HTTPException(status_code=404, detail="policy_chaos not found")
    return item

@router.post("/api/policy-chaos/{chaos_id}/verify")
async def api_policy_chaos_w130_verify_chaos(chaos_id: str, request: Request):
    """Verify chaos determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_chaos(chaos_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_chaos not found")
    return item
