"""Wave 47: Continuous Close 2.0 Router — Rolling exception queue, resumable idempotent jobs, background runners.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w47_continuous_close_v2 import service

router = APIRouter(tags=["Continuous Close 2.0"])

@router.get("/api/continuous-close-v2/exceptions")
async def api_continuous_close_v2_w47_job_exceptions(limit: int = 100):
    """Get rolling exceptions queue"""
    items = service.job_exceptions(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/continuous-close-v2/jobs")
async def api_continuous_close_v2_w47_list_jobs(limit: int = 100):
    """List continuous close jobs"""
    items = service.list_jobs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/continuous-close-v2/jobs", status_code=201)
async def api_continuous_close_v2_w47_start_job(request: Request):
    """Start a continuous close job"""
    data = await request.json()
    item = service.start_job(data)
    return item

@router.get("/api/continuous-close-v2/jobs/{job_id}")
async def api_continuous_close_v2_w47_get_job(job_id: str):
    """Get job details"""
    item = service.get_job(job_id)
    if not item:
        raise HTTPException(status_code=404, detail="continuous_close_v2 not found")
    return item

@router.post("/api/continuous-close-v2/jobs/{job_id}/cancel")
async def api_continuous_close_v2_w47_cancel_job(job_id: str, request: Request):
    """Cancel a job"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.cancel_job(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="continuous_close_v2 not found")
    return item

@router.post("/api/continuous-close-v2/jobs/{job_id}/pause")
async def api_continuous_close_v2_w47_pause_job(job_id: str, request: Request):
    """Pause a running job"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.pause_job(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="continuous_close_v2 not found")
    return item

@router.post("/api/continuous-close-v2/jobs/{job_id}/resume")
async def api_continuous_close_v2_w47_resume_job(job_id: str, request: Request):
    """Resume a paused job"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resume_job(job_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="continuous_close_v2 not found")
    return item
