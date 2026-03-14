"""Wave 10: Eval Harness Router — Evaluation framework for extraction and reconciliation quality.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w10_eval_harness import service

router = APIRouter(tags=["Eval Harness"])

@router.get("/api/evals")
async def api_list(limit: int = 100):
    """List evaluation runs"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/evals", status_code=201)
async def api_run_eval(request: Request):
    """Run an evaluation"""
    data = await request.json()
    item = service.run_eval(data)
    return item

@router.post("/api/evals/baseline", status_code=201)
async def api_baseline(request: Request):
    """Set evaluation baseline"""
    data = await request.json()
    item = service.baseline(data)
    return item

@router.get("/api/evals/compare")
async def api_compare(limit: int = 100):
    """Compare two evaluation runs"""
    items = service.compare(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/evals/{eval_id}")
async def api_get(eval_id: str):
    """Get evaluation results"""
    item = service.get(eval_id)
    if not item:
        raise HTTPException(status_code=404, detail="eval_harness not found")
    return item
