"""Wave 181: Gemini Live Provider v1 Router — Real Gemini Live provider behind ENABLE_GEMINI_LIVE flag. Connect/disconnect, stream transcript, interruption handling, tool calling hooks. DEMO uses simulator only.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w181_gemini_live_provider import service

router = APIRouter(tags=["Gemini Live Provider v1"])

@router.get("/api/gemini-live")
async def api_gemini_live_provider_w181_list_providers(limit: int = 100):
    """List Gemini Live provider configs"""
    items = service.list_providers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gemini-live", status_code=201)
async def api_gemini_live_provider_w181_create_provider(request: Request):
    """Create Gemini Live provider config"""
    data = await request.json()
    item = service.create_provider(data)
    return item

@router.get("/api/gemini-live/report")
async def api_gemini_live_provider_w181_provider_report(limit: int = 100):
    """Get provider report"""
    items = service.provider_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gemini-live/{provider_id}")
async def api_gemini_live_provider_w181_get_provider(provider_id: str):
    """Get provider details"""
    item = service.get_provider(provider_id)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_live_provider not found")
    return item

@router.post("/api/gemini-live/{provider_id}/connect")
async def api_gemini_live_provider_w181_connect_provider(provider_id: str, request: Request):
    """Connect provider via simulator shim"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.connect_provider(provider_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_live_provider not found")
    return item

@router.post("/api/gemini-live/{provider_id}/disconnect")
async def api_gemini_live_provider_w181_disconnect_provider(provider_id: str, request: Request):
    """Disconnect provider"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.disconnect_provider(provider_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_live_provider not found")
    return item

@router.get("/api/gemini-live/{provider_id}/transcript")
async def api_gemini_live_provider_w181_stream_transcript(provider_id: str):
    """Get transcript events"""
    item = service.stream_transcript(provider_id)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_live_provider not found")
    return item

@router.post("/api/gemini-live/{provider_id}/validate")
async def api_gemini_live_provider_w181_validate_config(provider_id: str, request: Request):
    """Validate provider config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_config(provider_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gemini_live_provider not found")
    return item
