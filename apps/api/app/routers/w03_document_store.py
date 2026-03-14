"""Wave 3: Document Store Router — Content-addressed document storage for invoices, receipts, statements.

PROJECT_ID: LEDGERLIVE
"""
import hashlib
import datetime as dt
from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from typing import Optional

from app.services.w03_document_store import service

router = APIRouter(tags=["Document Store"])

@router.get("/api/documents")
async def api_list(limit: int = 100):
    """List uploaded documents"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/documents", status_code=201)
async def api_upload(request: Request):
    """Upload a document — accepts JSON body or multipart form data."""
    content_type = request.headers.get("content-type", "")
    if "multipart" in content_type:
        form = await request.form()
        file_field = form.get("file")
        name = form.get("name", "uploaded_file")
        file_bytes = b""
        if file_field and hasattr(file_field, "read"):
            file_bytes = await file_field.read()
        data = {
            "filename": name if isinstance(name, str) else str(name),
            "content_hash": hashlib.sha256(file_bytes).hexdigest()[:16],
            "mime_type": getattr(file_field, "content_type", "application/octet-stream") if file_field else "application/octet-stream",
            "size_bytes": len(file_bytes),
            "uploaded_at": dt.datetime.utcnow().isoformat(),
            "entity_id": "upload",
        }
    else:
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
