"""Wave 180: Submission Hardening Wave Router — One-command local run, docs generator, expanded TOUR coverage. Documentation tests enforce commands exist. MCP E2E twice-run determinism.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w180_submission_harden import service

router = APIRouter(tags=["Submission Hardening Wave"])

@router.get("/api/submission-harden")
async def api_submission_harden_w180_list_checks(limit: int = 100):
    """List hardening checks"""
    items = service.list_checks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/submission-harden", status_code=201)
async def api_submission_harden_w180_run_check(request: Request):
    """Run hardening check"""
    data = await request.json()
    item = service.run_check(data)
    return item

@router.get("/api/submission-harden/report")
async def api_submission_harden_w180_harden_report(limit: int = 100):
    """Get hardening report"""
    items = service.harden_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/submission-harden/{harden_id}")
async def api_submission_harden_w180_get_check(harden_id: str):
    """Get check details"""
    item = service.get_check(harden_id)
    if not item:
        raise HTTPException(status_code=404, detail="submission_harden not found")
    return item

@router.post("/api/submission-harden/{harden_id}/determinism")
async def api_submission_harden_w180_verify_determinism(harden_id: str, request: Request):
    """Verify twice-run determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(harden_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="submission_harden not found")
    return item

@router.post("/api/submission-harden/{harden_id}/docs")
async def api_submission_harden_w180_verify_docs(harden_id: str, request: Request):
    """Verify docs match Make targets"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_docs(harden_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="submission_harden not found")
    return item
