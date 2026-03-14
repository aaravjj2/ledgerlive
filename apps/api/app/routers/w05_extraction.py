"""Wave 5: Data Extraction Router — Extract structured invoice/receipt fields from OCR text.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w05_extraction import service

router = APIRouter(tags=["Data Extraction"])

@router.get("/api/extractions")
async def api_list(limit: int = 100):
    """List extractions"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/extractions", status_code=201)
async def api_extract(request: Request):
    """Run extraction on OCR result"""
    data = await request.json()
    item = service.extract(data)
    return item

@router.get("/api/extractions/{extraction_id}")
async def api_get(extraction_id: str):
    """Get extraction result"""
    item = service.get(extraction_id)
    if not item:
        raise HTTPException(status_code=404, detail="extraction not found")
    return item

@router.put("/api/extractions/{extraction_id}")
async def api_correct(extraction_id: str, request: Request):
    """Correct extraction fields"""
    data = await request.json()
    item = service.correct(extraction_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="extraction not found")
    return item

@router.post("/api/extractions/{extraction_id}/validate")
async def api_validate(extraction_id: str, request: Request):
    """Validate extraction"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate(extraction_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="extraction not found")
    return item
