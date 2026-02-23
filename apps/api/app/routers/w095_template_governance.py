"""Wave 95: Template Governance Router — Template approval workflow with RBAC and version management.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w095_template_governance import service

router = APIRouter(tags=["Template Governance"])

@router.get("/api/template-governance")
async def api_template_governance_w95_list_requests(limit: int = 100):
    """List governance requests"""
    items = service.list_requests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/template-governance", status_code=201)
async def api_template_governance_w95_submit_request(request: Request):
    """Submit governance request"""
    data = await request.json()
    item = service.submit_request(data)
    return item

@router.get("/api/template-governance/report")
async def api_template_governance_w95_governance_report(limit: int = 100):
    """Get governance report"""
    items = service.governance_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/template-governance/{governance_id}")
async def api_template_governance_w95_get_request(governance_id: str):
    """Get request details"""
    item = service.get_request(governance_id)
    if not item:
        raise HTTPException(status_code=404, detail="template_governance not found")
    return item

@router.post("/api/template-governance/{governance_id}/approve")
async def api_template_governance_w95_approve(governance_id: str, request: Request):
    """Approve request"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve(governance_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="template_governance not found")
    return item

@router.post("/api/template-governance/{governance_id}/deny")
async def api_template_governance_w95_deny(governance_id: str, request: Request):
    """Deny request"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deny(governance_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="template_governance not found")
    return item
