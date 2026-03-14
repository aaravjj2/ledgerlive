"""Wave 330: Adversarial Corpus v3 Router — 100+ scenarios across channels/docs/blueprints with deterministic results.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w330_adversarial_corpus_v3 import service

router = APIRouter(tags=["Adversarial Corpus v3"])

@router.get("/api/adversarial-corpus-v3")
async def api_adversarial_corpus_v3_w330_list_corpora(limit: int = 100):
    """List adversarial corpora"""
    items = service.list_corpora(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/adversarial-corpus-v3", status_code=201)
async def api_adversarial_corpus_v3_w330_create_corpus(request: Request):
    """Create adversarial corpus"""
    data = await request.json()
    item = service.create_corpus(data)
    return item

@router.get("/api/adversarial-corpus-v3/report")
async def api_adversarial_corpus_v3_w330_corpus_report(limit: int = 100):
    """Get adversarial corpus report"""
    items = service.corpus_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/adversarial-corpus-v3/{corpus_id}")
async def api_adversarial_corpus_v3_w330_get_corpus(corpus_id: str):
    """Get corpus details"""
    item = service.get_corpus(corpus_id)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus_v3 not found")
    return item

@router.post("/api/adversarial-corpus-v3/{corpus_id}/analyze")
async def api_adversarial_corpus_v3_w330_analyze_results(corpus_id: str, request: Request):
    """Analyze results"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.analyze_results(corpus_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus_v3 not found")
    return item

@router.post("/api/adversarial-corpus-v3/{corpus_id}/run")
async def api_adversarial_corpus_v3_w330_run_scenarios(corpus_id: str, request: Request):
    """Run adversarial scenarios"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_scenarios(corpus_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus_v3 not found")
    return item
