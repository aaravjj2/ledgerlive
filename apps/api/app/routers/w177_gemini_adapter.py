"""Wave 177: Gemini Live Adapter Skeleton Router — Adapter interface compatible with Live Session Simulator. DEMO uses simulator; GEMINI provider behind flag with placeholder config.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w177_gemini_adapter import service

router = APIRouter(tags=["Gemini Live Adapter Skeleton"])

@router.get("/api/gemini-adapter")
async def api_gemini_adapter_w177_list_adapters(limit: int = 100):
    """List Gemini adapter configs"""
    items = service.list_adapters(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gemini-adapter", status_code=201)
async def api_gemini_adapter_w177_create_adapter(request: Request):
    """Create Gemini adapter config"""
    data = await request.json()
    item = service.create_adapter(data)
    return item

@router.get("/api/gemini-adapter/report")
async def api_gemini_adapter_w177_adapter_report(limit: int = 100):
    """Get adapter report"""
    items = service.adapter_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gemini-adapter/{adapter_id}")
async def api_gemini_adapter_w177_get_adapter(adapter_id: str):
    """Get adapter details"""
    item = service.get_adapter(adapter_id)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_adapter not found")
    return item

@router.post("/api/gemini-adapter/{adapter_id}/test")
async def api_gemini_adapter_w177_test_adapter(adapter_id: str, request: Request):
    """Test adapter offline"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_adapter(adapter_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_adapter not found")
    return item

@router.post("/api/gemini-adapter/{adapter_id}/validate")
async def api_gemini_adapter_w177_validate_config(adapter_id: str, request: Request):
    """Validate adapter config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_config(adapter_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_adapter not found")
    return item
