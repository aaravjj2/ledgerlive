"""Wave 115: Query Export E2E Router — MCP E2E for query execution and export log verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w115_query_export_e2e import service

router = APIRouter(tags=["Query Export E2E"])

@router.get("/api/query-export-e2e")
async def api_query_export_e2e_w115_list_tests(limit: int = 100):
    """List query export E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/query-export-e2e", status_code=201)
async def api_query_export_e2e_w115_start_test(request: Request):
    """Start query export E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/query-export-e2e/report")
async def api_query_export_e2e_w115_test_report(limit: int = 100):
    """Get query export E2E report"""
    items = service.test_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/query-export-e2e/{test_id}")
async def api_query_export_e2e_w115_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="query_export_e2e not found")
    return item

@router.post("/api/query-export-e2e/{test_id}/verify")
async def api_query_export_e2e_w115_verify(test_id: str, request: Request):
    """Verify export logs"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="query_export_e2e not found")
    return item
