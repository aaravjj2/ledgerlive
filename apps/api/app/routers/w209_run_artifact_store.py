"""Wave 209: Run Artifact Store v2 Router — Canonical replay artifacts for each close run: doc hashes, OCR text hashes, extraction outputs, transactions snapshot, tool plan, tool trace, approvals. Content-addressed.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w209_run_artifact_store import service

router = APIRouter(tags=["Run Artifact Store v2"])

@router.get("/api/run-artifacts")
async def api_run_artifact_store_w209_list_artifacts(limit: int = 100):
    """List run artifacts"""
    items = service.list_artifacts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/run-artifacts", status_code=201)
async def api_run_artifact_store_w209_store_artifact(request: Request):
    """Store canonical replay artifact"""
    data = await request.json()
    item = service.store_artifact(data)
    return item

@router.get("/api/run-artifacts/report")
async def api_run_artifact_store_w209_artifact_report(limit: int = 100):
    """Get artifact store report"""
    items = service.artifact_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/run-artifacts/{artifact_id}")
async def api_run_artifact_store_w209_get_artifact(artifact_id: str):
    """Get artifact details"""
    item = service.get_artifact(artifact_id)
    if not item:
        raise HTTPException(status_code=404, detail="run_artifact_store not found")
    return item

@router.post("/api/run-artifacts/{artifact_id}/restore")
async def api_run_artifact_store_w209_restore_snapshot(artifact_id: str, request: Request):
    """Restore snapshot from artifact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.restore_snapshot(artifact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="run_artifact_store not found")
    return item

@router.post("/api/run-artifacts/{artifact_id}/verify")
async def api_run_artifact_store_w209_verify_manifest(artifact_id: str, request: Request):
    """Verify artifact manifest hash"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_manifest(artifact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="run_artifact_store not found")
    return item
