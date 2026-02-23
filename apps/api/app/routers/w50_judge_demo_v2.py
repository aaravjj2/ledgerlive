"""Wave 50: Judge Demo 2.0 Router — Scripted 4-min demo script: seed, ingest, reconcile, override, export, verify.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w50_judge_demo_v2 import service

router = APIRouter(tags=["Judge Demo 2.0"])

@router.get("/api/judge-demo-v2/runs")
async def api_judge_demo_v2_w50_list_demos(limit: int = 100):
    """List demo runs"""
    items = service.list_demos(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/judge-demo-v2/runs", status_code=201)
async def api_judge_demo_v2_w50_start_demo(request: Request):
    """Start a scripted demo"""
    data = await request.json()
    item = service.start_demo(data)
    return item

@router.get("/api/judge-demo-v2/template")
async def api_judge_demo_v2_w50_script_template(limit: int = 100):
    """Get demo script template"""
    items = service.script_template(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/judge-demo-v2/runs/{demo_id}")
async def api_judge_demo_v2_w50_get_demo(demo_id: str):
    """Get demo run details"""
    item = service.get_demo(demo_id)
    if not item:
        raise HTTPException(status_code=404, detail="judge_demo_v2 not found")
    return item

@router.post("/api/judge-demo-v2/runs/{demo_id}/advance")
async def api_judge_demo_v2_w50_advance_step(demo_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_step(demo_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="judge_demo_v2 not found")
    return item

@router.post("/api/judge-demo-v2/runs/{demo_id}/reset")
async def api_judge_demo_v2_w50_reset_demo(demo_id: str, request: Request):
    """Reset demo state"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reset_demo(demo_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="judge_demo_v2 not found")
    return item

@router.post("/api/judge-demo-v2/runs/{demo_id}/verify")
async def api_judge_demo_v2_w50_verify_demo(demo_id: str, request: Request):
    """Verify demo hash determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_demo(demo_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="judge_demo_v2 not found")
    return item
