"""Wave 131: Seeded Chaos Matrix Router — Expanded chaos matrix: DB transient, storage fail, job interrupt, connector 429 (mocked).

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w131_chaos_matrix import service

router = APIRouter(tags=["Seeded Chaos Matrix"])

@router.get("/api/chaos-matrix")
async def api_chaos_matrix_w131_list_tests(limit: int = 100):
    """List chaos matrix tests"""
    items = service.list_tests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/chaos-matrix", status_code=201)
async def api_chaos_matrix_w131_run_test(request: Request):
    """Run chaos matrix test"""
    data = await request.json()
    item = service.run_test(data)
    return item

@router.get("/api/chaos-matrix/report")
async def api_chaos_matrix_w131_chaos_report(limit: int = 100):
    """Get chaos matrix report"""
    items = service.chaos_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/chaos-matrix/{test_id}")
async def api_chaos_matrix_w131_get_test(test_id: str):
    """Get test details"""
    item = service.get_test(test_id)
    if not item:
        raise HTTPException(status_code=404, detail="chaos_matrix not found")
    return item

@router.post("/api/chaos-matrix/{test_id}/inject")
async def api_chaos_matrix_w131_inject_failure(test_id: str, request: Request):
    """Inject specific failure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.inject_failure(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chaos_matrix not found")
    return item

@router.post("/api/chaos-matrix/{test_id}/verify")
async def api_chaos_matrix_w131_verify_determinism(test_id: str, request: Request):
    """Verify deterministic outcome"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(test_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="chaos_matrix not found")
    return item
