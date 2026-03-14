"""Wave 315: Atlassian E2E Suite v1 Router — MCP E2E: overdue approval -> Jira issue created -> visible on RC; export Confluence report preview.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w315_atlassian_e2e_suite import service

router = APIRouter(tags=["Atlassian E2E Suite v1"])

@router.get("/api/atlassian-e2e-suite")
async def api_atlassian_e2e_suite_w315_list_suites(limit: int = 100):
    """List E2E suites"""
    items = service.list_suites(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/atlassian-e2e-suite", status_code=201)
async def api_atlassian_e2e_suite_w315_run_suite(request: Request):
    """Run Atlassian E2E suite"""
    data = await request.json()
    item = service.run_suite(data)
    return item

@router.get("/api/atlassian-e2e-suite/report")
async def api_atlassian_e2e_suite_w315_suite_report(limit: int = 100):
    """Get Atlassian E2E report"""
    items = service.suite_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/atlassian-e2e-suite/{suite_id}")
async def api_atlassian_e2e_suite_w315_get_suite(suite_id: str):
    """Get suite details"""
    item = service.get_suite(suite_id)
    if not item:
        raise HTTPException(status_code=404, detail="atlassian_e2e_suite not found")
    return item

@router.post("/api/atlassian-e2e-suite/{suite_id}/export")
async def api_atlassian_e2e_suite_w315_export_results(suite_id: str, request: Request):
    """Export suite results"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_results(suite_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="atlassian_e2e_suite not found")
    return item

@router.post("/api/atlassian-e2e-suite/{suite_id}/rerun")
async def api_atlassian_e2e_suite_w315_rerun_suite(suite_id: str, request: Request):
    """Rerun E2E suite"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rerun_suite(suite_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="atlassian_e2e_suite not found")
    return item
