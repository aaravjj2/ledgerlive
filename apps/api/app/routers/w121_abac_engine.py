"""Wave 121: ABAC Policy Engine Router — Attribute-based access control with workspace/entity scopes and explainable denies.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w121_abac_engine import service

router = APIRouter(tags=["ABAC Policy Engine"])

@router.get("/api/abac-policies")
async def api_abac_engine_w121_list_policies(limit: int = 100):
    """List ABAC policies"""
    items = service.list_policies(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/abac-policies", status_code=201)
async def api_abac_engine_w121_create_policy(request: Request):
    """Create ABAC policy"""
    data = await request.json()
    item = service.create_policy(data)
    return item

@router.get("/api/abac-policies/matrix")
async def api_abac_engine_w121_policy_matrix(limit: int = 100):
    """Get policy evaluation matrix"""
    items = service.policy_matrix(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/abac-policies/{policy_id}")
async def api_abac_engine_w121_get_policy(policy_id: str):
    """Get policy details"""
    item = service.get_policy(policy_id)
    if not item:
        raise HTTPException(status_code=404, detail="abac_engine not found")
    return item

@router.post("/api/abac-policies/{policy_id}/evaluate")
async def api_abac_engine_w121_evaluate(policy_id: str, request: Request):
    """Evaluate policy against request"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="abac_engine not found")
    return item

@router.post("/api/abac-policies/{policy_id}/explain")
async def api_abac_engine_w121_explain_deny(policy_id: str, request: Request):
    """Explain deny reason"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.explain_deny(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="abac_engine not found")
    return item
