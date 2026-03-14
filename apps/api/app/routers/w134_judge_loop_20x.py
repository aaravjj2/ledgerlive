"""Wave 134: Judge Demo 20x Loop Router — 20x judge demo loop with determinism gate — all loops identical.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w134_judge_loop_20x import service

router = APIRouter(tags=["Judge Demo 20x Loop"])

@router.get("/api/judge-loop-20x")
async def api_judge_loop_20x_w134_list_loops(limit: int = 100):
    """List 20x loop runs"""
    items = service.list_loops(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/judge-loop-20x", status_code=201)
async def api_judge_loop_20x_w134_start_loop(request: Request):
    """Start 20x loop run"""
    data = await request.json()
    item = service.start_loop(data)
    return item

@router.get("/api/judge-loop-20x/report")
async def api_judge_loop_20x_w134_loop_report(limit: int = 100):
    """Get loop report"""
    items = service.loop_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/judge-loop-20x/{loop_id}")
async def api_judge_loop_20x_w134_get_loop(loop_id: str):
    """Get loop details"""
    item = service.get_loop(loop_id)
    if not item:
        raise HTTPException(status_code=404, detail="judge_loop_20x not found")
    return item

@router.post("/api/judge-loop-20x/{loop_id}/verify")
async def api_judge_loop_20x_w134_verify_hashes(loop_id: str, request: Request):
    """Verify all hashes identical"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_hashes(loop_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="judge_loop_20x not found")
    return item
