"""Wave 331: Security E2E Suite v1 Router — MCP E2E: injection attempt -> blocked -> remediation path -> approved -> proceeds safely.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w331_security_e2e_suite import service

router = APIRouter(tags=["Security E2E Suite v1"])

@router.get("/api/security-e2e-suite")
async def api_security_e2e_suite_w331_list_suites(limit: int = 100):
    """List security E2E suites"""
    items = service.list_suites(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-e2e-suite", status_code=201)
async def api_security_e2e_suite_w331_run_suite(request: Request):
    """Run security E2E suite"""
    data = await request.json()
    item = service.run_suite(data)
    return item

@router.get("/api/security-e2e-suite/report")
async def api_security_e2e_suite_w331_suite_report(limit: int = 100):
    """Get security E2E report"""
    items = service.suite_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-e2e-suite/{suite_id}")
async def api_security_e2e_suite_w331_get_suite(suite_id: str):
    """Get suite details"""
    item = service.get_suite(suite_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_e2e_suite not found")
    return item

@router.post("/api/security-e2e-suite/{suite_id}/evidence")
async def api_security_e2e_suite_w331_export_evidence(suite_id: str, request: Request):
    """Export security evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_evidence(suite_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_e2e_suite not found")
    return item

@router.post("/api/security-e2e-suite/{suite_id}/rerun")
async def api_security_e2e_suite_w331_rerun_suite(suite_id: str, request: Request):
    """Rerun E2E suite"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rerun_suite(suite_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_e2e_suite not found")
    return item
