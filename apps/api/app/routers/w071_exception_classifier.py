"""Wave 71: Exception Classifier Router — Deterministic rule-based exception classifier with suggested resolutions and evidence links.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w071_exception_classifier import service

router = APIRouter(tags=["Exception Classifier"])

@router.get("/api/exception-classifier")
async def api_exception_classifier_w71_list_classifications(limit: int = 100):
    """List classifications"""
    items = service.list_classifications(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/exception-classifier", status_code=201)
async def api_exception_classifier_w71_classify(request: Request):
    """Classify an exception"""
    data = await request.json()
    item = service.classify(data)
    return item

@router.get("/api/exception-classifier/stats")
async def api_exception_classifier_w71_classifier_stats(limit: int = 100):
    """Get classifier statistics"""
    items = service.classifier_stats(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/exception-classifier/{classification_id}")
async def api_exception_classifier_w71_get_classification(classification_id: str):
    """Get classification"""
    item = service.get_classification(classification_id)
    if not item:
        raise HTTPException(status_code=404, detail="exception_classifier not found")
    return item

@router.post("/api/exception-classifier/{classification_id}/apply")
async def api_exception_classifier_w71_apply_suggestion(classification_id: str, request: Request):
    """Apply suggested fix"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.apply_suggestion(classification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exception_classifier not found")
    return item

@router.post("/api/exception-classifier/{classification_id}/suggest")
async def api_exception_classifier_w71_suggest_fix(classification_id: str, request: Request):
    """Generate fix suggestion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.suggest_fix(classification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exception_classifier not found")
    return item
