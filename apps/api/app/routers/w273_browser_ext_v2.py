"""Wave 273: Browser Extension v2 Router — Capture, annotate, and submit with deterministic capture fixtures. Deep links to evidence with consistent rendering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w273_browser_ext_v2 import service

router = APIRouter(tags=["Browser Extension v2"])

@router.get("/api/browser-ext-v2")
async def api_browser_ext_v2_w273_list_captures(limit: int = 100):
    """List browser captures"""
    items = service.list_captures(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/browser-ext-v2", status_code=201)
async def api_browser_ext_v2_w273_create_capture(request: Request):
    """Create browser capture"""
    data = await request.json()
    item = service.create_capture(data)
    return item

@router.get("/api/browser-ext-v2/report")
async def api_browser_ext_v2_w273_capture_report(limit: int = 100):
    """Get browser extension report"""
    items = service.capture_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/browser-ext-v2/{capture_id}")
async def api_browser_ext_v2_w273_get_capture(capture_id: str):
    """Get capture details"""
    item = service.get_capture(capture_id)
    if not item:
        raise HTTPException(status_code=404, detail="browser_ext_v2 not found")
    return item

@router.post("/api/browser-ext-v2/{capture_id}/annotate")
async def api_browser_ext_v2_w273_annotate(capture_id: str, request: Request):
    """Add annotation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.annotate(capture_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="browser_ext_v2 not found")
    return item

@router.post("/api/browser-ext-v2/{capture_id}/submit")
async def api_browser_ext_v2_w273_submit_capture(capture_id: str, request: Request):
    """Submit capture as evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.submit_capture(capture_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="browser_ext_v2 not found")
    return item
