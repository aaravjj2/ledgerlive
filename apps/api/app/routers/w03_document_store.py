"""Wave 3: Document Store Router — Content-addressed document storage for invoices, receipts, statements.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w03_document_store import service

router = APIRouter(tags=["Document Store"])

@router.get("/api/documents")
async def api_list(limit: int = 100):
    """List uploaded documents"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/documents", status_code=201)
async def api_upload(request: Request):
    """Upload a document"""
    data = await request.json()
    item = service.upload(data)
    return item

@router.get("/api/documents/{doc_id}")
async def api_get(doc_id: str):
    """Get document metadata"""
    item = service.get(doc_id)
    if not item:
        raise HTTPException(status_code=404, detail="document_store not found")
    return item

@router.delete("/api/documents/{doc_id}")
async def api_delete_doc(doc_id: str):
    """Delete a document"""
    ok = service.delete_doc(doc_id)
    if not ok:
        raise HTTPException(status_code=404, detail="document_store not found")
    return {"deleted": True}

@router.get("/api/documents/{doc_id}/download")
async def api_download(doc_id: str):
    """Download document content"""
    item = service.download(doc_id)
    if not item:
        raise HTTPException(status_code=404, detail="document_store not found")
    return item
