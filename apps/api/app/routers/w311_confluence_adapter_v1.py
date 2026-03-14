"""Wave 311: Confluence Adapter v1 Router — Mock server generating Race Weekend Close Report pages from telemetry/court artifacts.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w311_confluence_adapter_v1 import service

router = APIRouter(tags=["Confluence Adapter v1"])

@router.get("/api/confluence-adapter")
async def api_confluence_adapter_v1_w311_list_pages(limit: int = 100):
    """List Confluence pages"""
    items = service.list_pages(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/confluence-adapter", status_code=201)
async def api_confluence_adapter_v1_w311_create_page(request: Request):
    """Create Confluence page"""
    data = await request.json()
    item = service.create_page(data)
    return item

@router.get("/api/confluence-adapter/report")
async def api_confluence_adapter_v1_w311_page_report(limit: int = 100):
    """Get Confluence adapter report"""
    items = service.page_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/confluence-adapter/{page_id}")
async def api_confluence_adapter_v1_w311_get_page(page_id: str):
    """Get page details"""
    item = service.get_page(page_id)
    if not item:
        raise HTTPException(status_code=404, detail="confluence_adapter_v1 not found")
    return item

@router.post("/api/confluence-adapter/{page_id}/preview")
async def api_confluence_adapter_v1_w311_render_preview(page_id: str, request: Request):
    """Render page preview"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.render_preview(page_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="confluence_adapter_v1 not found")
    return item

@router.post("/api/confluence-adapter/{page_id}/update")
async def api_confluence_adapter_v1_w311_update_content(page_id: str, request: Request):
    """Update page content"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.update_content(page_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="confluence_adapter_v1 not found")
    return item
