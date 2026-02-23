"""Wave 187: Connector Runbooks Anti-CI Guard Router — QBO/Xero/Plaid real-mode runbooks with explicit ENABLE flags and NEVER IN CI guard. Meta-test hard fails if CI env detected with ENABLE flags on.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w187_connector_runbooks import service

router = APIRouter(tags=["Connector Runbooks Anti-CI Guard"])

@router.get("/api/connector-runbooks")
async def api_connector_runbooks_w187_list_runbooks(limit: int = 100):
    """List connector runbooks"""
    items = service.list_runbooks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/connector-runbooks", status_code=201)
async def api_connector_runbooks_w187_create_runbook(request: Request):
    """Create connector runbook"""
    data = await request.json()
    item = service.create_runbook(data)
    return item

@router.get("/api/connector-runbooks/report")
async def api_connector_runbooks_w187_runbook_report(limit: int = 100):
    """Get runbook validation report"""
    items = service.runbook_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/connector-runbooks/{runbook_id}")
async def api_connector_runbooks_w187_get_runbook(runbook_id: str):
    """Get runbook details"""
    item = service.get_runbook(runbook_id)
    if not item:
        raise HTTPException(status_code=404, detail="connector_runbooks not found")
    return item

@router.post("/api/connector-runbooks/{runbook_id}/ci-guard")
async def api_connector_runbooks_w187_check_ci_guard(runbook_id: str, request: Request):
    """Check CI guard status"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_ci_guard(runbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_runbooks not found")
    return item

@router.post("/api/connector-runbooks/{runbook_id}/validate")
async def api_connector_runbooks_w187_validate_flags(runbook_id: str, request: Request):
    """Validate ENABLE flags"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_flags(runbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="connector_runbooks not found")
    return item
