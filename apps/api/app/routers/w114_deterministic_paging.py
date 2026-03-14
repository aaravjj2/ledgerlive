"""Wave 114: Deterministic Pagination Router — Guaranteed deterministic pagination and ordering for all list endpoints.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w114_deterministic_paging import service

router = APIRouter(tags=["Deterministic Pagination"])

@router.get("/api/deterministic-paging")
async def api_deterministic_paging_w114_list_tests(limit: int = 100):
    """List pagination tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/deterministic-paging", status_code=201)
async def api_deterministic_paging_w114_test_endpoint(request: Request):
    """Test endpoint pagination"""
    data = await request.json()
    item = service.test_endpoint(data)
    return item

@router.get("/api/deterministic-paging/report")
async def api_deterministic_paging_w114_paging_report(limit: int = 100):
    """Get pagination report"""
    items = service.paging_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/deterministic-paging/{page_id}")
async def api_deterministic_paging_w114_get_test(page_id: str):
    """Get test details"""
    item = service.get_test(page_id)
    if not item:
        raise HTTPException(status_code=404, detail="deterministic_paging not found")
    return item

@router.post("/api/deterministic-paging/{page_id}/verify")
async def api_deterministic_paging_w114_verify_order(page_id: str, request: Request):
    """Verify ordering consistency"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_order(page_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="deterministic_paging not found")
    return item
