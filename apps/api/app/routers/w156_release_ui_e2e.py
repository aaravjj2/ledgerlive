"""Wave 156: Release UI E2E Router — MCP E2E verifying release UI and artifact viewer.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w156_release_ui_e2e import service

router = APIRouter(tags=["Release UI E2E"])

@router.get("/api/release-ui-e2e")
async def api_release_ui_e2e_w156_list_tests(limit: int = 100):
    """List release UI E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/release-ui-e2e", status_code=201)
async def api_release_ui_e2e_w156_start_test(request: Request):
    """Start release UI E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/release-ui-e2e/report")
async def api_release_ui_e2e_w156_e2e_report(limit: int = 100):
    """Get release UI E2E report"""
    items = service.e2e_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/release-ui-e2e/{test_id}")
async def api_release_ui_e2e_w156_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_ui_e2e not found")
    return item

@router.post("/api/release-ui-e2e/{test_id}/verify")
async def api_release_ui_e2e_w156_verify_ui(test_id: str, request: Request):
    """Verify release UI"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_ui(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_ui_e2e not found")
    return item
