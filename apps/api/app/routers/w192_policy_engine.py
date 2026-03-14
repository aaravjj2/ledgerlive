"""Wave 192: Policy Engine v4 Router — Tool scopes tied to roles and data sensitivity. Approvals required for sensitive actions. Deterministic deny reasons with audit events.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w192_policy_engine import service

router = APIRouter(tags=["Policy Engine v4"])

@router.get("/api/policy-engine")
async def api_policy_engine_w192_list_policies(limit: int = 100):
    """List policy evaluations"""
    items = service.list_policies(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/policy-engine", status_code=201)
async def api_policy_engine_w192_evaluate_policy(request: Request):
    """Evaluate policy for action"""
    data = await request.json()
    item = service.evaluate_policy(data)
    return item

@router.get("/api/policy-engine/report")
async def api_policy_engine_w192_policy_report(limit: int = 100):
    """Get policy engine report"""
    items = service.policy_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/policy-engine/{policy_id}")
async def api_policy_engine_w192_get_policy(policy_id: str):
    """Get policy evaluation details"""
    item = service.get_policy(policy_id)
    if not item:
        raise HTTPException(status_code=404, detail="policy_engine not found")
    return item

@router.post("/api/policy-engine/{policy_id}/approve")
async def api_policy_engine_w192_approve_action(policy_id: str, request: Request):
    """Approve sensitive action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_action(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_engine not found")
    return item

@router.post("/api/policy-engine/{policy_id}/deny")
async def api_policy_engine_w192_deny_action(policy_id: str, request: Request):
    """Deny action with reason"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deny_action(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_engine not found")
    return item

@router.post("/api/policy-engine/{policy_id}/scope")
async def api_policy_engine_w192_check_scope(policy_id: str, request: Request):
    """Check tool scope for role"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_scope(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_engine not found")
    return item
