"""Wave 105: Key Management 3.0 Router — Key rotation with backward verifiability and key lifecycle management.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w105_key_management import service

router = APIRouter(tags=["Key Management 3.0"])

@router.get("/api/key-management")
async def api_key_management_w105_list_keys(limit: int = 100):
    """List keys"""
    items = service.list_keys(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/key-management", status_code=201)
async def api_key_management_w105_create_key(request: Request):
    """Create key"""
    data = await request.json()
    item = service.create_key(data)
    return item

@router.get("/api/key-management/lifecycle")
async def api_key_management_w105_key_lifecycle(limit: int = 100):
    """Get key lifecycle report"""
    items = service.key_lifecycle(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/key-management/{key_id}")
async def api_key_management_w105_get_key(key_id: str):
    """Get key details"""
    item = service.get_key(key_id)
    if not item:
        raise HTTPException(status_code=404, detail="key_management not found")
    return item

@router.post("/api/key-management/{key_id}/rotate")
async def api_key_management_w105_rotate_key(key_id: str, request: Request):
    """Rotate key"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rotate_key(key_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="key_management not found")
    return item

@router.post("/api/key-management/{key_id}/verify")
async def api_key_management_w105_verify_backward(key_id: str, request: Request):
    """Verify backward compatibility"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_backward(key_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="key_management not found")
    return item
