"""Wave 309: Jira Adapter v1 Router — Mock server creating issues for blockers/incidents/overdue approvals. Idempotent and deterministic.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w309_jira_adapter_v1 import service

router = APIRouter(tags=["Jira Adapter v1"])

@router.get("/api/jira-adapter")
async def api_jira_adapter_v1_w309_list_issues(limit: int = 100):
    """List Jira issues"""
    items = service.list_issues(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/jira-adapter", status_code=201)
async def api_jira_adapter_v1_w309_create_issue(request: Request):
    """Create Jira issue"""
    data = await request.json()
    item = service.create_issue(data)
    return item

@router.get("/api/jira-adapter/report")
async def api_jira_adapter_v1_w309_issue_report(limit: int = 100):
    """Get Jira adapter report"""
    items = service.issue_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/jira-adapter/{issue_id}")
async def api_jira_adapter_v1_w309_get_issue(issue_id: str):
    """Get issue details"""
    item = service.get_issue(issue_id)
    if not item:
        raise HTTPException(status_code=404, detail="jira_adapter_v1 not found")
    return item

@router.post("/api/jira-adapter/{issue_id}/resolve")
async def api_jira_adapter_v1_w309_resolve_issue(issue_id: str, request: Request):
    """Resolve issue"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve_issue(issue_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="jira_adapter_v1 not found")
    return item

@router.post("/api/jira-adapter/{issue_id}/transition")
async def api_jira_adapter_v1_w309_transition_issue(issue_id: str, request: Request):
    """Transition issue status"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.transition_issue(issue_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="jira_adapter_v1 not found")
    return item

@router.post("/api/jira-adapter/{issue_id}/update")
async def api_jira_adapter_v1_w309_update_issue(issue_id: str, request: Request):
    """Update issue"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.update_issue(issue_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="jira_adapter_v1 not found")
    return item
