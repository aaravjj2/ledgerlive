"""Wave 122: SSO/SCIM Mock Contracts Router — SSO and SCIM mocked contracts for CI-offline identity integration.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w122_sso_scim import service

router = APIRouter(tags=["SSO/SCIM Mock Contracts"])

@router.get("/api/sso-scim")
async def api_sso_scim_w122_list_contracts(limit: int = 100):
    """List SSO/SCIM contracts"""
    items = service.list_contracts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/sso-scim", status_code=201)
async def api_sso_scim_w122_create_contract(request: Request):
    """Create SSO/SCIM contract"""
    data = await request.json()
    item = service.create_contract(data)
    return item

@router.get("/api/sso-scim/report")
async def api_sso_scim_w122_contract_report(limit: int = 100):
    """Get SSO/SCIM report"""
    items = service.contract_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/sso-scim/{contract_id}")
async def api_sso_scim_w122_get_contract(contract_id: str):
    """Get contract details"""
    item = service.get_contract(contract_id)
    if not item:
        raise HTTPException(status_code=404, detail="sso_scim not found")
    return item

@router.post("/api/sso-scim/{contract_id}/map-roles")
async def api_sso_scim_w122_map_roles(contract_id: str, request: Request):
    """Map SSO roles"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.map_roles(contract_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="sso_scim not found")
    return item

@router.post("/api/sso-scim/{contract_id}/sync")
async def api_sso_scim_w122_sync_users(contract_id: str, request: Request):
    """Sync users via SCIM"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sync_users(contract_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="sso_scim not found")
    return item
