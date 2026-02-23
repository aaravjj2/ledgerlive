"""Wave 92: Workflow Template Marketplace Router — Import/export workflow templates with signature verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w092_workflow_marketplace import service

router = APIRouter(tags=["Workflow Template Marketplace"])

@router.get("/api/workflow-marketplace")
async def api_workflow_marketplace_w92_list_templates(limit: int = 100):
    """List marketplace templates"""
    items = service.list_templates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/workflow-marketplace", status_code=201)
async def api_workflow_marketplace_w92_publish(request: Request):
    """Publish workflow template"""
    data = await request.json()
    item = service.publish(data)
    return item

@router.get("/api/workflow-marketplace/export")
async def api_workflow_marketplace_w92_export_template(limit: int = 100):
    """Export templates bundle"""
    items = service.export_template(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/workflow-marketplace/{template_id}")
async def api_workflow_marketplace_w92_get_template(template_id: str):
    """Get template details"""
    item = service.get_template(template_id)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_marketplace not found")
    return item

@router.post("/api/workflow-marketplace/{template_id}/import")
async def api_workflow_marketplace_w92_import_template(template_id: str, request: Request):
    """Import template"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.import_template(template_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_marketplace not found")
    return item

@router.post("/api/workflow-marketplace/{template_id}/verify")
async def api_workflow_marketplace_w92_verify_template(template_id: str, request: Request):
    """Verify template signature"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_template(template_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow_marketplace not found")
    return item
