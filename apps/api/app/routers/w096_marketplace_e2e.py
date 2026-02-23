"""Wave 96: Marketplace E2E Router — MCP E2E marketplace flows: import→enable→run→export.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w096_marketplace_e2e import service

router = APIRouter(tags=["Marketplace E2E"])

@router.get("/api/marketplace-e2e")
async def api_marketplace_e2e_w96_list_tests(limit: int = 100):
    """List marketplace E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/marketplace-e2e", status_code=201)
async def api_marketplace_e2e_w96_start_test(request: Request):
    """Start marketplace E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/marketplace-e2e/report")
async def api_marketplace_e2e_w96_test_report(limit: int = 100):
    """Get marketplace E2E report"""
    items = service.test_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/marketplace-e2e/{test_id}")
async def api_marketplace_e2e_w96_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="marketplace_e2e not found")
    return item

@router.post("/api/marketplace-e2e/{test_id}/advance")
async def api_marketplace_e2e_w96_advance(test_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="marketplace_e2e not found")
    return item

@router.post("/api/marketplace-e2e/{test_id}/verify")
async def api_marketplace_e2e_w96_verify(test_id: str, request: Request):
    """Verify test completion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="marketplace_e2e not found")
    return item
