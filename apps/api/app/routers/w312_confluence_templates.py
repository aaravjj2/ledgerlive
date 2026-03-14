"""Wave 312: Confluence Page Templates v1 Router — Deterministic rendering with citations to dossiers and evidence artifacts.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w312_confluence_templates import service

router = APIRouter(tags=["Confluence Page Templates v1"])

@router.get("/api/confluence-templates")
async def api_confluence_templates_w312_list_templates(limit: int = 100):
    """List page templates"""
    items = service.list_templates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/confluence-templates", status_code=201)
async def api_confluence_templates_w312_create_template(request: Request):
    """Create page template"""
    data = await request.json()
    item = service.create_template(data)
    return item

@router.get("/api/confluence-templates/report")
async def api_confluence_templates_w312_template_report(limit: int = 100):
    """Get templates report"""
    items = service.template_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/confluence-templates/{template_id}")
async def api_confluence_templates_w312_get_template(template_id: str):
    """Get template details"""
    item = service.get_template(template_id)
    if not item:
        raise HTTPException(status_code=404, detail="confluence_templates not found")
    return item

@router.post("/api/confluence-templates/{template_id}/citations")
async def api_confluence_templates_w312_validate_citations(template_id: str, request: Request):
    """Validate citations"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_citations(template_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="confluence_templates not found")
    return item

@router.post("/api/confluence-templates/{template_id}/render")
async def api_confluence_templates_w312_render_template(template_id: str, request: Request):
    """Render template with data"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.render_template(template_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="confluence_templates not found")
    return item
