"""Wave 182: Cloud Run Deploy Automation Router — GCP Cloud Run deploy scripts for Agent Gateway. Smoke script hits healthz, runs simulator session, exports binder. Scripts are manual-only, never CI.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w182_cloudrun_deploy import service

router = APIRouter(tags=["Cloud Run Deploy Automation"])

@router.get("/api/cloudrun-deploy")
async def api_cloudrun_deploy_w182_list_deploys(limit: int = 100):
    """List deploy configs"""
    items = service.list_deploys(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/cloudrun-deploy", status_code=201)
async def api_cloudrun_deploy_w182_create_deploy(request: Request):
    """Create deploy config"""
    data = await request.json()
    item = service.create_deploy(data)
    return item

@router.get("/api/cloudrun-deploy/report")
async def api_cloudrun_deploy_w182_deploy_report(limit: int = 100):
    """Get deploy validation report"""
    items = service.deploy_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cloudrun-deploy/{deploy_id}")
async def api_cloudrun_deploy_w182_get_deploy(deploy_id: str):
    """Get deploy details"""
    item = service.get_deploy(deploy_id)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy not found")
    return item

@router.post("/api/cloudrun-deploy/{deploy_id}/smoke-plan")
async def api_cloudrun_deploy_w182_generate_smoke_plan(deploy_id: str, request: Request):
    """Generate smoke test plan"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_smoke_plan(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy not found")
    return item

@router.post("/api/cloudrun-deploy/{deploy_id}/smoke-schema")
async def api_cloudrun_deploy_w182_validate_smoke_schema(deploy_id: str, request: Request):
    """Validate smoke report schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_smoke_schema(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy not found")
    return item

@router.post("/api/cloudrun-deploy/{deploy_id}/validate")
async def api_cloudrun_deploy_w182_validate_scripts(deploy_id: str, request: Request):
    """Validate deploy scripts structure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_scripts(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy not found")
    return item
