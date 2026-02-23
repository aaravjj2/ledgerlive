"""Wave 167: Close Orchestrator Workflow v1 Router — Full close orchestrator DAG: ingest, OCR, extraction, recon, triage, approvals, binder, verify, board pack. Resumable and idempotent by job_id.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w167_close_orchestrator import service

router = APIRouter(tags=["Close Orchestrator Workflow v1"])

@router.get("/api/close-orchestrator/jobs")
async def api_close_orchestrator_w167_list_jobs(limit: int = 100):
    """List orchestrator jobs"""
    items = service.list_jobs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-orchestrator/jobs", status_code=201)
async def api_close_orchestrator_w167_start_job(request: Request):
    """Start close orchestrator job"""
    data = await request.json()
    item = service.start_job(data)
    return item

@router.get("/api/close-orchestrator/report")
async def api_close_orchestrator_w167_job_report(limit: int = 100):
    """Get orchestrator report"""
    items = service.job_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-orchestrator/jobs/{job_id}")
async def api_close_orchestrator_w167_get_job(job_id: str):
    """Get job details"""
    item = service.get_job(job_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_orchestrator not found")
    return item

@router.post("/api/close-orchestrator/jobs/{job_id}/advance")
async def api_close_orchestrator_w167_advance_step(job_id: str, request: Request):
    """Advance to next DAG step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_step(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_orchestrator not found")
    return item

@router.post("/api/close-orchestrator/jobs/{job_id}/binder")
async def api_close_orchestrator_w167_export_binder(job_id: str, request: Request):
    """Export binder from job"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_binder(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_orchestrator not found")
    return item

@router.post("/api/close-orchestrator/jobs/{job_id}/resume")
async def api_close_orchestrator_w167_resume_job(job_id: str, request: Request):
    """Resume failed job"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resume_job(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_orchestrator not found")
    return item

@router.post("/api/close-orchestrator/jobs/{job_id}/verify")
async def api_close_orchestrator_w167_verify_outputs(job_id: str, request: Request):
    """Verify all step outputs"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_outputs(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_orchestrator not found")
    return item
