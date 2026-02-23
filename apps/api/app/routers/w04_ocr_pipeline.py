"""Wave 4: OCR Pipeline Router — Deterministic DEMO OCR pipeline for document text extraction.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w04_ocr_pipeline import service

router = APIRouter(tags=["OCR Pipeline"])

@router.get("/api/ocr-jobs")
async def api_list(limit: int = 100):
    """List OCR jobs"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ocr-jobs", status_code=201)
async def api_submit(request: Request):
    """Submit document for OCR"""
    data = await request.json()
    item = service.submit(data)
    return item

@router.get("/api/ocr-jobs/stats")
async def api_stats(limit: int = 100):
    """OCR pipeline statistics"""
    items = service.stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ocr-jobs/{ocr_id}")
async def api_get(ocr_id: str):
    """Get OCR job result"""
    item = service.get(ocr_id)
    if not item:
        raise HTTPException(status_code=404, detail="ocr_pipeline not found")
    return item

@router.post("/api/ocr-jobs/{ocr_id}/retry")
async def api_retry(ocr_id: str, request: Request):
    """Retry failed OCR job"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.retry(ocr_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ocr_pipeline not found")
    return item
