"""Wave 147: UI Pagination Determinism Router — UI pagination, filtering, and stable ordering verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w147_ui_pagination import service

router = APIRouter(tags=["UI Pagination Determinism"])

@router.get("/api/ui-pagination")
async def api_ui_pagination_w147_list_tests(limit: int = 100):
    """List pagination tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ui-pagination", status_code=201)
async def api_ui_pagination_w147_test_pagination(request: Request):
    """Test pagination determinism"""
    data = await request.json()
    item = service.test_pagination(data)
    return item

@router.get("/api/ui-pagination/report")
async def api_ui_pagination_w147_pagination_report(limit: int = 100):
    """Get pagination report"""
    items = service.pagination_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ui-pagination/{test_id}")
async def api_ui_pagination_w147_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="ui_pagination not found")
    return item

@router.post("/api/ui-pagination/{test_id}/verify")
async def api_ui_pagination_w147_verify_ordering(test_id: str, request: Request):
    """Verify ordering stability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_ordering(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ui_pagination not found")
    return item
