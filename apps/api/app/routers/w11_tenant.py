"""Wave 11: Multi-Tenant Management Router — Tenant isolation and management for multi-org deployment.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w11_tenant import service

router = APIRouter(tags=["Multi-Tenant Management"])

@router.get("/api/tenants")
async def api_list(limit: int = 100):
    """List all tenants"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tenants", status_code=201)
async def api_create(request: Request):
    """Create a tenant"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/tenants/{tenant_id}")
async def api_get(tenant_id: str):
    """Get tenant details"""
    item = service.get(tenant_id)
    if not item:
        raise HTTPException(status_code=404, detail="tenant not found")
    return item

@router.put("/api/tenants/{tenant_id}")
async def api_update(tenant_id: str, request: Request):
    """Update tenant"""
    data = await request.json()
    item = service.update(tenant_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tenant not found")
    return item

@router.post("/api/tenants/{tenant_id}/suspend")
async def api_suspend(tenant_id: str, request: Request):
    """Suspend a tenant"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.suspend(tenant_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tenant not found")
    return item
