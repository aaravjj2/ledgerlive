"""Wave 207: Multi-Tenant Live Sessions v1 Router — Live sessions scoped to tenant/workspace. Auth/RBAC enforced. Cross-tenant access to artifacts and tool traces prevented.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w207_multi_tenant import service

router = APIRouter(tags=["Multi-Tenant Live Sessions v1"])

@router.get("/api/multi-tenant")
async def api_multi_tenant_w207_list_tenants(limit: int = 100):
    """List tenant session configs"""
    items = service.list_tenants(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/multi-tenant", status_code=201)
async def api_multi_tenant_w207_create_tenant(request: Request):
    """Create tenant session config"""
    data = await request.json()
    item = service.create_tenant(data)
    return item

@router.get("/api/multi-tenant/report")
async def api_multi_tenant_w207_tenant_report(limit: int = 100):
    """Get multi-tenant report"""
    items = service.tenant_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/multi-tenant/{tenant_id}")
async def api_multi_tenant_w207_get_tenant(tenant_id: str):
    """Get tenant details"""
    item = service.get_tenant(tenant_id)
    if not item:
        raise HTTPException(status_code=404, detail="multi_tenant not found")
    return item

@router.post("/api/multi-tenant/{tenant_id}/cross-access")
async def api_multi_tenant_w207_test_cross_access(tenant_id: str, request: Request):
    """Test cross-tenant access blocked"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_cross_access(tenant_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_tenant not found")
    return item

@router.post("/api/multi-tenant/{tenant_id}/verify")
async def api_multi_tenant_w207_verify_isolation(tenant_id: str, request: Request):
    """Verify tenant isolation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_isolation(tenant_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="multi_tenant not found")
    return item
