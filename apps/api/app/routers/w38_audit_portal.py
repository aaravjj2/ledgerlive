"""Wave 38: Audit Portal Router — Auditor role with saved queries, export logs, and immutable Q&A log.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w38_audit_portal import service

router = APIRouter(tags=["Audit Portal"])

@router.get("/api/audit-portal/export")
async def api_audit_portal_w38_export_log(limit: int = 100):
    """Export audit portal log"""
    items = service.export_log(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/audit-portal/queries")
async def api_audit_portal_w38_list_queries(limit: int = 100):
    """List saved audit queries"""
    items = service.list_queries(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-portal/queries", status_code=201)
async def api_audit_portal_w38_create_query(request: Request):
    """Create a saved query"""
    data = await request.json()
    item = service.create_query(data)
    return item

@router.get("/api/audit-portal/queries/{query_id}")
async def api_audit_portal_w38_get_query(query_id: str):
    """Get query details"""
    item = service.get_query(query_id)
    if not item:
        raise HTTPException(status_code=404, detail="audit_portal not found")
    return item

@router.post("/api/audit-portal/queries/{query_id}/execute")
async def api_audit_portal_w38_execute_query(query_id: str, request: Request):
    """Execute a saved query"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.execute_query(query_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_portal not found")
    return item

@router.post("/api/audit-portal/queries/{query_id}/qa")
async def api_audit_portal_w38_add_qa(query_id: str, request: Request):
    """Add Q&A to audit log"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_qa(query_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_portal not found")
    return item
