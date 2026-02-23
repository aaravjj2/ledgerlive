"""Wave 80: Exception Flow E2E Router — MCP E2E for exception resolution end-to-end flow with determinism verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w080_exc_flow_e2e import service

router = APIRouter(tags=["Exception Flow E2E"])

@router.get("/api/exc-flow-e2e")
async def api_exc_flow_e2e_w80_list_tests(limit: int = 100):
    """List exception flow E2E tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/exc-flow-e2e", status_code=201)
async def api_exc_flow_e2e_w80_start_test(request: Request):
    """Start exception flow E2E test"""
    data = await request.json()
    item = service.start_test(data)
    return item

@router.get("/api/exc-flow-e2e/report")
async def api_exc_flow_e2e_w80_test_report(limit: int = 100):
    """Get exception flow E2E report"""
    items = service.test_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/exc-flow-e2e/{test_id}")
async def api_exc_flow_e2e_w80_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="exc_flow_e2e not found")
    return item

@router.post("/api/exc-flow-e2e/{test_id}/advance")
async def api_exc_flow_e2e_w80_advance(test_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exc_flow_e2e not found")
    return item

@router.post("/api/exc-flow-e2e/{test_id}/verify")
async def api_exc_flow_e2e_w80_verify(test_id: str, request: Request):
    """Verify determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exc_flow_e2e not found")
    return item
