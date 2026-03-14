"""Wave 219: Hackathon Checklist Auto-Verifier v1 Router — Checklists for Gemini/Airia/DO/Automation hackathons. make verify-hackathons checks repo artifacts and bundles offline. Deterministic report.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w219_checklist_verifier import service

router = APIRouter(tags=["Hackathon Checklist Auto-Verifier v1"])

@router.get("/api/checklist-verifier")
async def api_checklist_verifier_w219_list_checks(limit: int = 100):
    """List checklist verifications"""
    items = service.list_checks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/checklist-verifier", status_code=201)
async def api_checklist_verifier_w219_run_check(request: Request):
    """Run hackathon checklist verification"""
    data = await request.json()
    item = service.run_check(data)
    return item

@router.get("/api/checklist-verifier/report")
async def api_checklist_verifier_w219_check_report(limit: int = 100):
    """Get checklist verification report"""
    items = service.check_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/checklist-verifier/{check_id}")
async def api_checklist_verifier_w219_get_check(check_id: str):
    """Get check details"""
    item = service.get_check(check_id)
    if not item:
        raise HTTPException(status_code=404, detail="checklist_verifier not found")
    return item

@router.post("/api/checklist-verifier/{check_id}/fail")
async def api_checklist_verifier_w219_trigger_failure(check_id: str, request: Request):
    """Trigger missing item failure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.trigger_failure(check_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="checklist_verifier not found")
    return item

@router.post("/api/checklist-verifier/{check_id}/verify")
async def api_checklist_verifier_w219_verify_item(check_id: str, request: Request):
    """Verify individual checklist item"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_item(check_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="checklist_verifier not found")
    return item
