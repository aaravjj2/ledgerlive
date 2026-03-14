"""Wave 183: Session Interruption Resume Safety Router — Idempotent job keys for live tool calls. Session interruption cannot duplicate side effects. Resume endpoint continues from last checkpoint.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w183_session_resume import service

router = APIRouter(tags=["Session Interruption Resume Safety"])

@router.get("/api/session-resume")
async def api_session_resume_w183_list_resumes(limit: int = 100):
    """List session resume records"""
    items = service.list_resumes(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/session-resume", status_code=201)
async def api_session_resume_w183_create_session_run(request: Request):
    """Start a resumable session run"""
    data = await request.json()
    item = service.create_session_run(data)
    return item

@router.get("/api/session-resume/report")
async def api_session_resume_w183_resume_report(limit: int = 100):
    """Get session resume report"""
    items = service.resume_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/session-resume/{resume_id}")
async def api_session_resume_w183_get_resume(resume_id: str):
    """Get resume record details"""
    item = service.get_resume(resume_id)
    if not item:
        raise HTTPException(status_code=404, detail="session_resume not found")
    return item

@router.post("/api/session-resume/{resume_id}/interrupt")
async def api_session_resume_w183_interrupt_session(resume_id: str, request: Request):
    """Force interrupt session"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.interrupt_session(resume_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="session_resume not found")
    return item

@router.post("/api/session-resume/{resume_id}/resume")
async def api_session_resume_w183_resume_session(resume_id: str, request: Request):
    """Resume session from checkpoint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resume_session(resume_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="session_resume not found")
    return item

@router.post("/api/session-resume/{resume_id}/verify")
async def api_session_resume_w183_verify_idempotency(resume_id: str, request: Request):
    """Verify no duplicate side effects"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_idempotency(resume_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="session_resume not found")
    return item
