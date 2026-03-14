"""Wave 144: Large Fixture E2E Smoke Router — MCP E2E smoke tests on large fixtures to verify UI performance.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w144_large_fixture_e2e import service

router = APIRouter(tags=["Large Fixture E2E Smoke"])

@router.get("/api/large-fixture-e2e")
async def api_large_fixture_e2e_w144_list_tests(limit: int = 100):
    """List large fixture E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/large-fixture-e2e", status_code=201)
async def api_large_fixture_e2e_w144_start_test(request: Request):
    """Start large fixture E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/large-fixture-e2e/report")
async def api_large_fixture_e2e_w144_smoke_report(limit: int = 100):
    """Get large fixture smoke report"""
    items = service.smoke_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/large-fixture-e2e/{test_id}")
async def api_large_fixture_e2e_w144_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="large_fixture_e2e not found")
    return item

@router.post("/api/large-fixture-e2e/{test_id}/verify")
async def api_large_fixture_e2e_w144_verify_perf(test_id: str, request: Request):
    """Verify performance budgets"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_perf(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="large_fixture_e2e not found")
    return item
