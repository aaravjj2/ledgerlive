"""Wave 259: Adversarial Corpus v2 Router — 50+ scenarios across channels and tools that must all deterministically block or require approval. Expanded coverage with evidence-backed decisions.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w259_adversarial_corpus_v2 import service

router = APIRouter(tags=["Adversarial Corpus v2"])

@router.get("/api/adversarial-corpus-v2")
async def api_adversarial_corpus_v2_w259_list_corpora(limit: int = 100):
    """List adversarial corpora"""
    items = service.list_corpora(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/adversarial-corpus-v2", status_code=201)
async def api_adversarial_corpus_v2_w259_create_corpus(request: Request):
    """Create adversarial corpus"""
    data = await request.json()
    item = service.create_corpus(data)
    return item

@router.get("/api/adversarial-corpus-v2/report")
async def api_adversarial_corpus_v2_w259_corpus_report(limit: int = 100):
    """Get adversarial corpus report"""
    items = service.corpus_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/adversarial-corpus-v2/{corpus_id}")
async def api_adversarial_corpus_v2_w259_get_corpus(corpus_id: str):
    """Get corpus details"""
    item = service.get_corpus(corpus_id)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus_v2 not found")
    return item

@router.post("/api/adversarial-corpus-v2/{corpus_id}/run")
async def api_adversarial_corpus_v2_w259_run_scenarios(corpus_id: str, request: Request):
    """Run all scenarios"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_scenarios(corpus_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus_v2 not found")
    return item

@router.post("/api/adversarial-corpus-v2/{corpus_id}/verify-determinism")
async def api_adversarial_corpus_v2_w259_verify_determinism(corpus_id: str, request: Request):
    """Verify deterministic results"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(corpus_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus_v2 not found")
    return item
