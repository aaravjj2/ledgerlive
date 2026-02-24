"""Wave 267: Audit Q&A Pack v1 Router — Question template with linked evidence for auditor portal integration. One-click generation with deterministic content.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w267_audit_qa_pack import service

router = APIRouter(tags=["Audit Q&A Pack v1"])

@router.get("/api/audit-qa-pack")
async def api_audit_qa_pack_w267_list_qa_packs(limit: int = 100):
    """List audit Q&A packs"""
    items = service.list_qa_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-qa-pack", status_code=201)
async def api_audit_qa_pack_w267_create_qa_pack(request: Request):
    """Create audit Q&A pack"""
    data = await request.json()
    item = service.create_qa_pack(data)
    return item

@router.get("/api/audit-qa-pack/report")
async def api_audit_qa_pack_w267_qa_report(limit: int = 100):
    """Get audit Q&A pack report"""
    items = service.qa_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/audit-qa-pack/{qa_id}")
async def api_audit_qa_pack_w267_get_qa_pack(qa_id: str):
    """Get Q&A pack details"""
    item = service.get_qa_pack(qa_id)
    if not item:
        raise HTTPException(status_code=404, detail="audit_qa_pack not found")
    return item

@router.post("/api/audit-qa-pack/{qa_id}/evidence")
async def api_audit_qa_pack_w267_link_evidence(qa_id: str, request: Request):
    """Link evidence to answer"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_evidence(qa_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_qa_pack not found")
    return item

@router.post("/api/audit-qa-pack/{qa_id}/question")
async def api_audit_qa_pack_w267_add_question(qa_id: str, request: Request):
    """Add question to pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_question(qa_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_qa_pack not found")
    return item
