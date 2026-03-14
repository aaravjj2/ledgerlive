"""Wave 125: Policy Regression Suite Router — Deny reason stability and policy regression testing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w125_policy_regression import service

router = APIRouter(tags=["Policy Regression Suite"])

@router.get("/api/policy-regressions")
async def api_policy_regression_w125_list_regressions(limit: int = 100):
    """List policy regressions"""
    items = service.list_regressions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/policy-regressions", status_code=201)
async def api_policy_regression_w125_run_regression(request: Request):
    """Run policy regression test"""
    data = await request.json()
    item = service.run_regression(data)
    return item

@router.get("/api/policy-regressions/report")
async def api_policy_regression_w125_regression_report(limit: int = 100):
    """Get regression report"""
    items = service.regression_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/policy-regressions/{regression_id}")
async def api_policy_regression_w125_get_regression(regression_id: str):
    """Get regression details"""
    item = service.get_regression(regression_id)
    if not item:
        raise HTTPException(status_code=404, detail="policy_regression not found")
    return item

@router.post("/api/policy-regressions/{regression_id}/verify")
async def api_policy_regression_w125_verify_stability(regression_id: str, request: Request):
    """Verify deny stability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_stability(regression_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_regression not found")
    return item
