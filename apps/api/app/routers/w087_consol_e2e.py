"""Wave 87: Consolidation E2E Router — MCP E2E for consolidation scenarios: 2+ entities, intercompany, FX, export verify.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w087_consol_e2e import service

router = APIRouter(tags=["Consolidation E2E"])

@router.get("/api/consol-e2e")
async def api_consol_e2e_w87_list_tests(limit: int = 100):
    """List consolidation E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/consol-e2e", status_code=201)
async def api_consol_e2e_w87_start_test(request: Request):
    """Start consolidation E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/consol-e2e/report")
async def api_consol_e2e_w87_test_report(limit: int = 100):
    """Get consolidation E2E report"""
    items = service.test_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/consol-e2e/{test_id}")
async def api_consol_e2e_w87_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="consol_e2e not found")
    return item

@router.post("/api/consol-e2e/{test_id}/verify")
async def api_consol_e2e_w87_verify_export(test_id: str, request: Request):
    """Verify export hash"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_export(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_e2e not found")
    return item
