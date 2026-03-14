"""Wave 107: Compliance E2E Router — MCP E2E: auditor portal + compliance exports + verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w107_compliance_e2e import service

router = APIRouter(tags=["Compliance E2E"])

@router.get("/api/compliance-e2e")
async def api_compliance_e2e_w107_list_tests(limit: int = 100):
    """List compliance E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/compliance-e2e", status_code=201)
async def api_compliance_e2e_w107_start_test(request: Request):
    """Start compliance E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/compliance-e2e/report")
async def api_compliance_e2e_w107_test_report(limit: int = 100):
    """Get compliance E2E report"""
    items = service.test_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/compliance-e2e/{test_id}")
async def api_compliance_e2e_w107_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_e2e not found")
    return item

@router.post("/api/compliance-e2e/{test_id}/verify")
async def api_compliance_e2e_w107_verify_export(test_id: str, request: Request):
    """Verify compliance export"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_export(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_e2e not found")
    return item
