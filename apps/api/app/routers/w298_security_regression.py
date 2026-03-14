"""Wave 298: Security Regression Budgets v1 Router — Fail if injection/exfil detection coverage or deny explainability regresses. Deterministic regression tracking.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w298_security_regression import service

router = APIRouter(tags=["Security Regression Budgets v1"])

@router.get("/api/security-regression")
async def api_security_regression_w298_list_regressions(limit: int = 100):
    """List security regressions"""
    items = service.list_regressions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-regression", status_code=201)
async def api_security_regression_w298_create_regression(request: Request):
    """Create security regression check"""
    data = await request.json()
    item = service.create_regression(data)
    return item

@router.get("/api/security-regression/report")
async def api_security_regression_w298_regression_report(limit: int = 100):
    """Get security regression report"""
    items = service.regression_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-regression/{regression_id}")
async def api_security_regression_w298_get_regression(regression_id: str):
    """Get regression details"""
    item = service.get_regression(regression_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_regression not found")
    return item

@router.post("/api/security-regression/{regression_id}/coverage")
async def api_security_regression_w298_measure_coverage(regression_id: str, request: Request):
    """Measure detection coverage"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure_coverage(regression_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_regression not found")
    return item

@router.post("/api/security-regression/{regression_id}/explainability")
async def api_security_regression_w298_measure_explainability(regression_id: str, request: Request):
    """Measure deny explainability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure_explainability(regression_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_regression not found")
    return item
