"""Wave 320: Race Theme Pack v2 Router — Ensure Race Control naming is consistent across bundles and UI.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w320_race_theme_pack_v2 import service

router = APIRouter(tags=["Race Theme Pack v2"])

@router.get("/api/race-theme-pack-v2")
async def api_race_theme_pack_v2_w320_list_themes(limit: int = 100):
    """List theme packs"""
    items = service.list_themes(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/race-theme-pack-v2", status_code=201)
async def api_race_theme_pack_v2_w320_create_theme(request: Request):
    """Create theme pack check"""
    data = await request.json()
    item = service.create_theme(data)
    return item

@router.get("/api/race-theme-pack-v2/report")
async def api_race_theme_pack_v2_w320_theme_report(limit: int = 100):
    """Get theme pack report"""
    items = service.theme_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/race-theme-pack-v2/{theme_id}")
async def api_race_theme_pack_v2_w320_get_theme(theme_id: str):
    """Get theme details"""
    item = service.get_theme(theme_id)
    if not item:
        raise HTTPException(status_code=404, detail="race_theme_pack_v2 not found")
    return item

@router.post("/api/race-theme-pack-v2/{theme_id}/check")
async def api_race_theme_pack_v2_w320_check_consistency(theme_id: str, request: Request):
    """Check naming consistency"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_consistency(theme_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="race_theme_pack_v2 not found")
    return item

@router.post("/api/race-theme-pack-v2/{theme_id}/fix")
async def api_race_theme_pack_v2_w320_apply_fixes(theme_id: str, request: Request):
    """Apply naming fixes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_fixes(theme_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="race_theme_pack_v2 not found")
    return item
