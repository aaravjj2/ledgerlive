"""Wave 45: Mapping Studio 2.0 Router — Deterministic transform DSL for imports: vendor mapping, COA mapping, tax mapping.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w45_mapping_studio import service

router = APIRouter(tags=["Mapping Studio 2.0"])

@router.get("/api/mapping-studio/export")
async def api_mapping_studio_w45_export_rules(limit: int = 100):
    """Export all mapping rules"""
    items = service.export_rules(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/mapping-studio/rules")
async def api_mapping_studio_w45_list_rules(limit: int = 100):
    """List mapping rules"""
    items = service.list_rules(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/mapping-studio/rules", status_code=201)
async def api_mapping_studio_w45_create_rule(request: Request):
    """Create a mapping rule"""
    data = await request.json()
    item = service.create_rule(data)
    return item

@router.get("/api/mapping-studio/rules/{rule_id}")
async def api_mapping_studio_w45_get_rule(rule_id: str):
    """Get rule details"""
    item = service.get_rule(rule_id)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_studio not found")
    return item

@router.post("/api/mapping-studio/rules/{rule_id}/apply")
async def api_mapping_studio_w45_apply_rule(rule_id: str, request: Request):
    """Apply mapping rule"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_rule(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_studio not found")
    return item

@router.post("/api/mapping-studio/rules/{rule_id}/preview")
async def api_mapping_studio_w45_preview(rule_id: str, request: Request):
    """Preview rule application"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.preview(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_studio not found")
    return item

@router.post("/api/mapping-studio/rules/{rule_id}/rollback")
async def api_mapping_studio_w45_rollback(rule_id: str, request: Request):
    """Rollback rule version"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="mapping_studio not found")
    return item
