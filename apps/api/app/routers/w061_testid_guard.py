"""Wave 61: TestID Guard Router — Meta-guard ensuring every route has page-root data-testid. Fails build if missing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w061_testid_guard import service

router = APIRouter(tags=["TestID Guard"])

@router.get("/api/testid-guards")
async def api_testid_guard_w61_list_guards(limit: int = 100):
    """List testid guard checks"""
    items = service.list_guards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/testid-guards", status_code=201)
async def api_testid_guard_w61_run_scan(request: Request):
    """Run testid scan on all routes"""
    data = await request.json()
    item = service.run_scan(data)
    return item

@router.get("/api/testid-guards/coverage")
async def api_testid_guard_w61_coverage_report(limit: int = 100):
    """Get testid coverage report"""
    items = service.coverage_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/testid-guards/{guard_id}")
async def api_testid_guard_w61_get_guard(guard_id: str):
    """Get guard result details"""
    item = service.get_guard(guard_id)
    if not item:
        raise HTTPException(status_code=404, detail="testid_guard not found")
    return item

@router.post("/api/testid-guards/{guard_id}/fix")
async def api_testid_guard_w61_fix_missing(guard_id: str, request: Request):
    """Apply missing testid fixes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.fix_missing(guard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="testid_guard not found")
    return item
