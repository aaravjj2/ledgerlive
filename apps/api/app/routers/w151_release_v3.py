"""Wave 151: Release Bundle 3.0 Router — Release bundle v3 with full proof inventory and multi-layer signatures.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w151_release_v3 import service

router = APIRouter(tags=["Release Bundle 3.0"])

@router.get("/api/releases-v3")
async def api_release_v3_w151_list_releases(limit: int = 100):
    """List releases v3"""
    items = service.list_releases(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/releases-v3", status_code=201)
async def api_release_v3_w151_create_release(request: Request):
    """Create release v3"""
    data = await request.json()
    item = service.create_release(data)
    return item

@router.get("/api/releases-v3/export")
async def api_release_v3_w151_export_release(limit: int = 100):
    """Export release v3 bundle"""
    items = service.export_release(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/releases-v3/{release_id}")
async def api_release_v3_w151_get_release(release_id: str):
    """Get release v3 details"""
    item = service.get_release(release_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_v3 not found")
    return item

@router.post("/api/releases-v3/{release_id}/sign")
async def api_release_v3_w151_sign_release(release_id: str, request: Request):
    """Sign release v3"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_release(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_v3 not found")
    return item

@router.post("/api/releases-v3/{release_id}/verify")
async def api_release_v3_w151_verify_release(release_id: str, request: Request):
    """Verify release integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_release(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_v3 not found")
    return item
