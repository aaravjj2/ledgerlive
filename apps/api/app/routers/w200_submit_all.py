"""Wave 200: Submission Hardening v2 Router — Single command generator: make submit-all produces all bundles and index. Docs match Make targets. TOUR >=240s coverage. Twice-run determinism.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w200_submit_all import service

router = APIRouter(tags=["Submission Hardening v2"])

@router.get("/api/submit-all")
async def api_submit_all_w200_list_submissions(limit: int = 100):
    """List submission checks"""
    items = service.list_submissions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/submit-all", status_code=201)
async def api_submit_all_w200_run_submission(request: Request):
    """Run submission hardening check"""
    data = await request.json()
    item = service.run_submission(data)
    return item

@router.get("/api/submit-all/report")
async def api_submit_all_w200_submission_report(limit: int = 100):
    """Get submission hardening report"""
    items = service.submission_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/submit-all/{submission_id}")
async def api_submit_all_w200_get_submission(submission_id: str):
    """Get submission details"""
    item = service.get_submission(submission_id)
    if not item:
        raise HTTPException(status_code=404, detail="submit_all not found")
    return item

@router.post("/api/submit-all/{submission_id}/determinism")
async def api_submit_all_w200_verify_determinism(submission_id: str, request: Request):
    """Verify twice-run determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(submission_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="submit_all not found")
    return item

@router.post("/api/submit-all/{submission_id}/docs")
async def api_submit_all_w200_verify_docs(submission_id: str, request: Request):
    """Verify docs match Make targets"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_docs(submission_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="submit_all not found")
    return item
