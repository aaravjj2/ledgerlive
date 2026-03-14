"""Wave 196: DigitalOcean Deploy Automation v1 Router — DO App Platform/container deployment scripts. Smoke runs health check, sim session, binder export, hackpack export. Deterministic smoke format.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w196_do_deploy import service

router = APIRouter(tags=["DigitalOcean Deploy Automation v1"])

@router.get("/api/do-deploy")
async def api_do_deploy_w196_list_deploys(limit: int = 100):
    """List DO deploy configs"""
    items = service.list_deploys(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/do-deploy", status_code=201)
async def api_do_deploy_w196_create_deploy(request: Request):
    """Create DO deploy config"""
    data = await request.json()
    item = service.create_deploy(data)
    return item

@router.get("/api/do-deploy/report")
async def api_do_deploy_w196_deploy_report(limit: int = 100):
    """Get DO deploy report"""
    items = service.deploy_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/do-deploy/{deploy_id}")
async def api_do_deploy_w196_get_deploy(deploy_id: str):
    """Get deploy details"""
    item = service.get_deploy(deploy_id)
    if not item:
        raise HTTPException(status_code=404, detail="do_deploy not found")
    return item

@router.post("/api/do-deploy/{deploy_id}/smoke")
async def api_do_deploy_w196_generate_smoke(deploy_id: str, request: Request):
    """Generate smoke report schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_smoke(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="do_deploy not found")
    return item

@router.post("/api/do-deploy/{deploy_id}/validate")
async def api_do_deploy_w196_validate_config(deploy_id: str, request: Request):
    """Validate DO deploy config"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_config(deploy_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="do_deploy not found")
    return item
