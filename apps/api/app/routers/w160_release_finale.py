"""Wave 160: Release Finale Router — Tag v0.160.0-ledgerlive with PASS proof pack — the determinism finale.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w160_release_finale import service

router = APIRouter(tags=["Release Finale"])

@router.get("/api/release-finales")
async def api_release_finale_w160_list_finales(limit: int = 100):
    """List release finales"""
    items = service.list_finales(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/release-finales", status_code=201)
async def api_release_finale_w160_create_finale(request: Request):
    """Create release finale"""
    data = await request.json()
    item = service.create_finale(data)
    return item

@router.get("/api/release-finales/report")
async def api_release_finale_w160_finale_report(limit: int = 100):
    """Get finale report"""
    items = service.finale_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/release-finales/{finale_id}")
async def api_release_finale_w160_get_finale(finale_id: str):
    """Get finale details"""
    item = service.get_finale(finale_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_finale not found")
    return item

@router.post("/api/release-finales/{finale_id}/sign")
async def api_release_finale_w160_sign_finale(finale_id: str, request: Request):
    """Sign finale release"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_finale(finale_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_finale not found")
    return item

@router.post("/api/release-finales/{finale_id}/verify")
async def api_release_finale_w160_verify_finale(finale_id: str, request: Request):
    """Verify finale proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_finale(finale_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_finale not found")
    return item
