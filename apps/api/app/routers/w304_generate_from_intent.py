"""Wave 304: Generate from Intent v1 Router — Deterministic rules engine generates a blueprint from a short intent description (no LLM required).

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w304_generate_from_intent import service

router = APIRouter(tags=["Generate from Intent v1"])

@router.get("/api/generate-from-intent")
async def api_generate_from_intent_w304_list_intents(limit: int = 100):
    """List generated intents"""
    items = service.list_intents(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/generate-from-intent", status_code=201)
async def api_generate_from_intent_w304_generate_blueprint(request: Request):
    """Generate blueprint from intent"""
    data = await request.json()
    item = service.generate_blueprint(data)
    return item

@router.get("/api/generate-from-intent/report")
async def api_generate_from_intent_w304_intent_report(limit: int = 100):
    """Get intent generation report"""
    items = service.intent_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/generate-from-intent/{intent_id}")
async def api_generate_from_intent_w304_get_intent(intent_id: str):
    """Get intent details"""
    item = service.get_intent(intent_id)
    if not item:
        raise HTTPException(status_code=404, detail="generate_from_intent not found")
    return item

@router.post("/api/generate-from-intent/{intent_id}/preview")
async def api_generate_from_intent_w304_preview_intent(intent_id: str, request: Request):
    """Preview generated blueprint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.preview_intent(intent_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="generate_from_intent not found")
    return item

@router.post("/api/generate-from-intent/{intent_id}/refine")
async def api_generate_from_intent_w304_refine_intent(intent_id: str, request: Request):
    """Refine generated blueprint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.refine_intent(intent_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="generate_from_intent not found")
    return item
