"""Wave 24: Data Retention Router — Policy-based data retention and archival.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w24_retention import service

router = APIRouter(tags=["Data Retention"])

@router.get("/api/retention/policies")
async def api_list_policies(limit: int = 100):
    """List retention policies"""
    items = service.list_policies(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/retention/policies", status_code=201)
async def api_create_policy(request: Request):
    """Create a retention policy"""
    data = await request.json()
    item = service.create_policy(data)
    return item

@router.get("/api/retention/policies/{policy_id}")
async def api_get_policy(policy_id: str):
    """Get policy details"""
    item = service.get_policy(policy_id)
    if not item:
        raise HTTPException(status_code=404, detail="retention not found")
    return item

@router.post("/api/retention/policies/{policy_id}/preview")
async def api_preview(policy_id: str, request: Request):
    """Preview affected records"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.preview(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="retention not found")
    return item

@router.post("/api/retention/policies/{policy_id}/run")
async def api_run_policy(policy_id: str, request: Request):
    """Run retention policy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_policy(policy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="retention not found")
    return item
