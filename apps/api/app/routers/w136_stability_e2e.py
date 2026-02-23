"""Wave 136: MCP Stability E2E Router — MCP E2E stability suite: re-run flows repeatedly and verify consistency.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w136_stability_e2e import service

router = APIRouter(tags=["MCP Stability E2E"])

@router.get("/api/stability-e2e")
async def api_stability_e2e_w136_list_tests(limit: int = 100):
    """List stability E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/stability-e2e", status_code=201)
async def api_stability_e2e_w136_start_test(request: Request):
    """Start stability E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/stability-e2e/report")
async def api_stability_e2e_w136_stability_report(limit: int = 100):
    """Get stability report"""
    items = service.stability_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/stability-e2e/{test_id}")
async def api_stability_e2e_w136_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="stability_e2e not found")
    return item

@router.post("/api/stability-e2e/{test_id}/verify")
async def api_stability_e2e_w136_verify_consistency(test_id: str, request: Request):
    """Verify consistency"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_consistency(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="stability_e2e not found")
    return item
