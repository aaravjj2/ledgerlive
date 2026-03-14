"""Wave 322: Readiness E2E Suite v1 Router — MCP E2E: generate bundle -> validate -> verify -> show PASS badge.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w322_readiness_e2e_suite import service

router = APIRouter(tags=["Readiness E2E Suite v1"])

@router.get("/api/readiness-e2e-suite")
async def api_readiness_e2e_suite_w322_list_suites(limit: int = 100):
    """List E2E suites"""
    items = service.list_suites(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/readiness-e2e-suite", status_code=201)
async def api_readiness_e2e_suite_w322_run_suite(request: Request):
    """Run readiness E2E suite"""
    data = await request.json()
    item = service.run_suite(data)
    return item

@router.get("/api/readiness-e2e-suite/report")
async def api_readiness_e2e_suite_w322_suite_report(limit: int = 100):
    """Get readiness E2E report"""
    items = service.suite_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/readiness-e2e-suite/{suite_id}")
async def api_readiness_e2e_suite_w322_get_suite(suite_id: str):
    """Get suite details"""
    item = service.get_suite(suite_id)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_e2e_suite not found")
    return item

@router.post("/api/readiness-e2e-suite/{suite_id}/badge")
async def api_readiness_e2e_suite_w322_export_badge(suite_id: str, request: Request):
    """Export PASS badge"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_badge(suite_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_e2e_suite not found")
    return item

@router.post("/api/readiness-e2e-suite/{suite_id}/rerun")
async def api_readiness_e2e_suite_w322_rerun_suite(suite_id: str, request: Request):
    """Rerun E2E suite"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rerun_suite(suite_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_e2e_suite not found")
    return item
