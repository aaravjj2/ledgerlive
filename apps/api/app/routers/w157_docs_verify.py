"""Wave 157: Documentation & VERIFY.md Router — Documentation polish and VERIFY.md generation for release verification guide.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w157_docs_verify import service

router = APIRouter(tags=["Documentation & VERIFY.md"])

@router.get("/api/docs-verify")
async def api_docs_verify_w157_list_docs(limit: int = 100):
    """List verification docs"""
    items = service.list_docs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/docs-verify", status_code=201)
async def api_docs_verify_w157_generate_doc(request: Request):
    """Generate verification doc"""
    data = await request.json()
    item = service.generate_doc(data)
    return item

@router.get("/api/docs-verify/export")
async def api_docs_verify_w157_export_docs(limit: int = 100):
    """Export verification docs"""
    items = service.export_docs(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/docs-verify/{doc_id}")
async def api_docs_verify_w157_get_doc(doc_id: str):
    """Get doc details"""
    item = service.get_doc(doc_id)
    if not item:
        raise HTTPException(status_code=404, detail="docs_verify not found")
    return item

@router.post("/api/docs-verify/{doc_id}/verify")
async def api_docs_verify_w157_verify_doc(doc_id: str, request: Request):
    """Verify doc accuracy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_doc(doc_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="docs_verify not found")
    return item
