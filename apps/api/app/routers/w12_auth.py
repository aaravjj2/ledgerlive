"""Wave 12: Authentication & RBAC Router — User authentication and role-based access control.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w12_auth import service

router = APIRouter(tags=["Authentication & RBAC"])

@router.get("/api/auth/users")
async def api_list_users(limit: int = 100):
    """List users"""
    items = service.list_users(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/auth/users", status_code=201)
async def api_create_user(request: Request):
    """Create a user"""
    data = await request.json()
    item = service.create_user(data)
    return item

@router.get("/api/auth/users/{user_id}")
async def api_get_user(user_id: str):
    """Get user details"""
    item = service.get_user(user_id)
    if not item:
        raise HTTPException(status_code=404, detail="auth not found")
    return item

@router.post("/api/auth/users/{user_id}/deactivate")
async def api_deactivate_user(user_id: str, request: Request):
    """Deactivate user"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deactivate_user(user_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="auth not found")
    return item

@router.put("/api/auth/users/{user_id}/role")
async def api_update_role(user_id: str, request: Request):
    """Update user role"""
    data = await request.json()
    item = service.update_role(user_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="auth not found")
    return item
