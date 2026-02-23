"""Wave 198: Deployed Environment Chaos Hooks Router — Optional deployed chaos run scripts for GCP/DO. Never executed in CI. Config and validator only in CI. Seeded chaos for deployed environments.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w198_chaos_hooks import service

router = APIRouter(tags=["Deployed Environment Chaos Hooks"])

@router.get("/api/chaos-hooks")
async def api_chaos_hooks_w198_list_hooks(limit: int = 100):
    """List chaos hook configs"""
    items = service.list_hooks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/chaos-hooks", status_code=201)
async def api_chaos_hooks_w198_create_hook(request: Request):
    """Create chaos hook config"""
    data = await request.json()
    item = service.create_hook(data)
    return item

@router.get("/api/chaos-hooks/report")
async def api_chaos_hooks_w198_hook_report(limit: int = 100):
    """Get chaos hooks report"""
    items = service.hook_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/chaos-hooks/{hook_id}")
async def api_chaos_hooks_w198_get_hook(hook_id: str):
    """Get hook details"""
    item = service.get_hook(hook_id)
    if not item:
        raise HTTPException(status_code=404, detail="chaos_hooks not found")
    return item

@router.post("/api/chaos-hooks/{hook_id}/ci-check")
async def api_chaos_hooks_w198_check_ci_safety(hook_id: str, request: Request):
    """Check hook is CI safe"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_ci_safety(hook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chaos_hooks not found")
    return item

@router.post("/api/chaos-hooks/{hook_id}/validate")
async def api_chaos_hooks_w198_validate_hook(hook_id: str, request: Request):
    """Validate hook script exists and is safe"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_hook(hook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chaos_hooks not found")
    return item
