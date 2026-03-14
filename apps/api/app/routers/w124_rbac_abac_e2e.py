"""Wave 124: RBAC/ABAC E2E Router — MCP E2E for full RBAC/ABAC matrix validation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w124_rbac_abac_e2e import service

router = APIRouter(tags=["RBAC/ABAC E2E"])

@router.get("/api/rbac-abac-e2e")
async def api_rbac_abac_e2e_w124_list_tests(limit: int = 100):
    """List RBAC/ABAC E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rbac-abac-e2e", status_code=201)
async def api_rbac_abac_e2e_w124_start_test(request: Request):
    """Start RBAC/ABAC E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/rbac-abac-e2e/report")
async def api_rbac_abac_e2e_w124_test_report(limit: int = 100):
    """Get RBAC/ABAC E2E report"""
    items = service.test_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rbac-abac-e2e/{test_id}")
async def api_rbac_abac_e2e_w124_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="rbac_abac_e2e not found")
    return item

@router.post("/api/rbac-abac-e2e/{test_id}/verify")
async def api_rbac_abac_e2e_w124_verify_matrix(test_id: str, request: Request):
    """Verify permission matrix"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_matrix(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rbac_abac_e2e not found")
    return item
