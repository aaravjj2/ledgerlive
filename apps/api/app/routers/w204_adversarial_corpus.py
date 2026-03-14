"""Wave 204: Agent Policy Adversarial Corpus v1 Router — Adversarial prompt corpus and tool misuse scenarios: bypass approvals, export without dossier, change locked periods. Policy engine blocks with deterministic reasons.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w204_adversarial_corpus import service

router = APIRouter(tags=["Agent Policy Adversarial Corpus v1"])

@router.get("/api/adversarial-corpus")
async def api_adversarial_corpus_w204_list_corpus(limit: int = 100):
    """List adversarial corpus scenarios"""
    items = service.list_corpus(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/adversarial-corpus", status_code=201)
async def api_adversarial_corpus_w204_add_scenario(request: Request):
    """Add adversarial scenario"""
    data = await request.json()
    item = service.add_scenario(data)
    return item

@router.get("/api/adversarial-corpus/report")
async def api_adversarial_corpus_w204_corpus_report(limit: int = 100):
    """Get adversarial corpus report"""
    items = service.corpus_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/adversarial-corpus/{corpus_id}")
async def api_adversarial_corpus_w204_get_scenario(corpus_id: str):
    """Get scenario details"""
    item = service.get_scenario(corpus_id)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus not found")
    return item

@router.post("/api/adversarial-corpus/{corpus_id}/run")
async def api_adversarial_corpus_w204_run_scenario(corpus_id: str, request: Request):
    """Run adversarial scenario"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_scenario(corpus_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus not found")
    return item

@router.post("/api/adversarial-corpus/{corpus_id}/verify")
async def api_adversarial_corpus_w204_verify_blocked(corpus_id: str, request: Request):
    """Verify scenario was blocked"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_blocked(corpus_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="adversarial_corpus not found")
    return item
