"""Wave 306: Template Validator v3 Router — Strict completeness checks with deterministic checksums for compiled templates.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w306_template_validator_v3 import service

router = APIRouter(tags=["Template Validator v3"])

@router.get("/api/template-validator-v3")
async def api_template_validator_v3_w306_list_validations(limit: int = 100):
    """List template validations"""
    items = service.list_validations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/template-validator-v3", status_code=201)
async def api_template_validator_v3_w306_validate_template(request: Request):
    """Validate template"""
    data = await request.json()
    item = service.validate_template(data)
    return item

@router.get("/api/template-validator-v3/report")
async def api_template_validator_v3_w306_validation_report(limit: int = 100):
    """Get validation report"""
    items = service.validation_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/template-validator-v3/{validation_id}")
async def api_template_validator_v3_w306_get_validation(validation_id: str):
    """Get validation details"""
    item = service.get_validation(validation_id)
    if not item:
        raise HTTPException(status_code=404, detail="template_validator_v3 not found")
    return item

@router.post("/api/template-validator-v3/{validation_id}/checksum")
async def api_template_validator_v3_w306_checksum_verify(validation_id: str, request: Request):
    """Verify template checksum"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.checksum_verify(validation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="template_validator_v3 not found")
    return item

@router.post("/api/template-validator-v3/{validation_id}/revalidate")
async def api_template_validator_v3_w306_revalidate(validation_id: str, request: Request):
    """Revalidate template"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.revalidate(validation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="template_validator_v3 not found")
    return item
