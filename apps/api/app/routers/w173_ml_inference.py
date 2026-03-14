"""Wave 173: ML Inference Hook v1 Router — Model-driven routing: low-confidence extracts to review, auto-suggest triage, auto-approve low-risk matches with verifier gating and explainability.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w173_ml_inference import service

router = APIRouter(tags=["ML Inference Hook v1"])

@router.get("/api/ml-inference")
async def api_ml_inference_w173_list_inferences(limit: int = 100):
    """List inference results"""
    items = service.list_inferences(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ml-inference", status_code=201)
async def api_ml_inference_w173_run_inference(request: Request):
    """Run ML inference"""
    data = await request.json()
    item = service.run_inference(data)
    return item

@router.get("/api/ml-inference/report")
async def api_ml_inference_w173_inference_report(limit: int = 100):
    """Get inference report"""
    items = service.inference_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ml-inference/{inference_id}")
async def api_ml_inference_w173_get_inference(inference_id: str):
    """Get inference details"""
    item = service.get_inference(inference_id)
    if not item:
        raise HTTPException(status_code=404, detail="ml_inference not found")
    return item

@router.post("/api/ml-inference/{inference_id}/explain")
async def api_ml_inference_w173_explain_decision(inference_id: str, request: Request):
    """Get explainability report"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.explain_decision(inference_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_inference not found")
    return item

@router.post("/api/ml-inference/{inference_id}/fallback")
async def api_ml_inference_w173_fallback_check(inference_id: str, request: Request):
    """Check fallback behavior"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.fallback_check(inference_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_inference not found")
    return item
