"""Wave 220: Submission Hardening v3 Router — make submit-all outputs gemini/airia/do/automation bundles with index and checksums. TOUR >=240s covering parity, replay, court pack, impact, verifier, submit.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w220_submit_all_v3 import service

router = APIRouter(tags=["Submission Hardening v3"])

@router.get("/api/submit-all-v3")
async def api_submit_all_v3_w220_list_submissions(limit: int = 100):
    """List submission bundles"""
    items = service.list_submissions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/submit-all-v3", status_code=201)
async def api_submit_all_v3_w220_generate_submission(request: Request):
    """Generate submission bundle"""
    data = await request.json()
    item = service.generate_submission(data)
    return item

@router.get("/api/submit-all-v3/report")
async def api_submit_all_v3_w220_submission_report(limit: int = 100):
    """Get submission hardening report"""
    items = service.submission_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/submit-all-v3/{submission_id}")
async def api_submit_all_v3_w220_get_submission(submission_id: str):
    """Get submission details"""
    item = service.get_submission(submission_id)
    if not item:
        raise HTTPException(status_code=404, detail="submit_all_v3 not found")
    return item

@router.post("/api/submit-all-v3/{submission_id}/determinism")
async def api_submit_all_v3_w220_verify_determinism(submission_id: str, request: Request):
    """Verify twice-run determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(submission_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="submit_all_v3 not found")
    return item

@router.post("/api/submit-all-v3/{submission_id}/verify")
async def api_submit_all_v3_w220_verify_bundle(submission_id: str, request: Request):
    """Verify bundle completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_bundle(submission_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="submit_all_v3 not found")
    return item
