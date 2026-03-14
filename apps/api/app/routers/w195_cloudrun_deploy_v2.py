"""Wave 195: Cloud Run Deploy v2 Router — Deploy scripts for LedgerLive API+Web and agent gateway on GCP. Smoke script produces deterministic smoke_report.json. Manual only.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w195_cloudrun_deploy_v2 import service

router = APIRouter(tags=["Cloud Run Deploy v2"])

@router.get("/api/cloudrun-v2")
async def api_cloudrun_deploy_v2_w195_list_deploys(limit: int = 100):
    """List Cloud Run v2 deploy configs"""
    items = service.list_deploys(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/cloudrun-v2", status_code=201)
async def api_cloudrun_deploy_v2_w195_create_deploy(request: Request):
    """Create deploy config"""
    data = await request.json()
    item = service.create_deploy(data)
    return item

@router.get("/api/cloudrun-v2/report")
async def api_cloudrun_deploy_v2_w195_deploy_report(limit: int = 100):
    """Get deploy validation report"""
    items = service.deploy_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cloudrun-v2/{deploy_id}")
async def api_cloudrun_deploy_v2_w195_get_deploy(deploy_id: str):
    """Get deploy details"""
    item = service.get_deploy(deploy_id)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy_v2 not found")
    return item

@router.post("/api/cloudrun-v2/{deploy_id}/smoke")
async def api_cloudrun_deploy_v2_w195_generate_smoke(deploy_id: str, request: Request):
    """Generate smoke report schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_smoke(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy_v2 not found")
    return item

@router.post("/api/cloudrun-v2/{deploy_id}/validate")
async def api_cloudrun_deploy_v2_w195_validate_config(deploy_id: str, request: Request):
    """Validate deploy config + scripts"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_config(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cloudrun_deploy_v2 not found")
    return item
