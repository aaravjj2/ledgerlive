"""Wave 208: Fail-Closed Posture v1 Router — If verifier cannot prove invariants or evidence missing, action becomes approval required or blocked. Never auto-approve under uncertainty.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w208_fail_closed import service

router = APIRouter(tags=["Fail-Closed Posture v1"])

@router.get("/api/fail-closed")
async def api_fail_closed_w208_list_postures(limit: int = 100):
    """List fail-closed evaluations"""
    items = service.list_postures(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/fail-closed", status_code=201)
async def api_fail_closed_w208_evaluate_posture(request: Request):
    """Evaluate fail-closed posture"""
    data = await request.json()
    item = service.evaluate_posture(data)
    return item

@router.get("/api/fail-closed/report")
async def api_fail_closed_w208_posture_report(limit: int = 100):
    """Get fail-closed posture report"""
    items = service.posture_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/fail-closed/{posture_id}")
async def api_fail_closed_w208_get_posture(posture_id: str):
    """Get posture details"""
    item = service.get_posture(posture_id)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed not found")
    return item

@router.post("/api/fail-closed/{posture_id}/trigger")
async def api_fail_closed_w208_trigger_fail_closed(posture_id: str, request: Request):
    """Trigger fail-closed scenario"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.trigger_fail_closed(posture_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed not found")
    return item

@router.post("/api/fail-closed/{posture_id}/verify")
async def api_fail_closed_w208_verify_blocked(posture_id: str, request: Request):
    """Verify action was blocked"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_blocked(posture_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fail_closed not found")
    return item
