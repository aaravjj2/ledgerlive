"""Wave 318: Airia Bundle Validator v3 Router — Publish readiness strict check with deterministic file ordering and checksums.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w318_airia_bundle_validator_v3 import service

router = APIRouter(tags=["Airia Bundle Validator v3"])

@router.get("/api/airia-bundle-validator-v3")
async def api_airia_bundle_validator_v3_w318_list_validations(limit: int = 100):
    """List bundle validations"""
    items = service.list_validations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/airia-bundle-validator-v3", status_code=201)
async def api_airia_bundle_validator_v3_w318_validate_bundle(request: Request):
    """Validate bundle for readiness"""
    data = await request.json()
    item = service.validate_bundle(data)
    return item

@router.get("/api/airia-bundle-validator-v3/report")
async def api_airia_bundle_validator_v3_w318_validation_report(limit: int = 100):
    """Get validation report"""
    items = service.validation_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/airia-bundle-validator-v3/{validation_id}")
async def api_airia_bundle_validator_v3_w318_get_validation(validation_id: str):
    """Get validation details"""
    item = service.get_validation(validation_id)
    if not item:
        raise HTTPException(status_code=404, detail="airia_bundle_validator_v3 not found")
    return item

@router.post("/api/airia-bundle-validator-v3/{validation_id}/fix-ordering")
async def api_airia_bundle_validator_v3_w318_fix_ordering(validation_id: str, request: Request):
    """Fix file ordering"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.fix_ordering(validation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_bundle_validator_v3 not found")
    return item

@router.post("/api/airia-bundle-validator-v3/{validation_id}/revalidate")
async def api_airia_bundle_validator_v3_w318_revalidate(validation_id: str, request: Request):
    """Revalidate bundle"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.revalidate(validation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_bundle_validator_v3 not found")
    return item
