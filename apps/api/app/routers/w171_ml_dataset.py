"""Wave 171: ML Dataset Builder v1 Router — Deterministic dataset builder from seeded close runs: extraction labels, match labels, exception categories. Output with sha256 manifest.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w171_ml_dataset import service

router = APIRouter(tags=["ML Dataset Builder v1"])

@router.get("/api/ml-datasets")
async def api_ml_dataset_w171_list_datasets(limit: int = 100):
    """List ML datasets"""
    items = service.list_datasets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ml-datasets", status_code=201)
async def api_ml_dataset_w171_generate_dataset(request: Request):
    """Generate ML dataset from fixtures"""
    data = await request.json()
    item = service.generate_dataset(data)
    return item

@router.get("/api/ml-datasets/report")
async def api_ml_dataset_w171_dataset_report(limit: int = 100):
    """Get dataset generation report"""
    items = service.dataset_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ml-datasets/{dataset_id}")
async def api_ml_dataset_w171_get_dataset(dataset_id: str):
    """Get dataset details"""
    item = service.get_dataset(dataset_id)
    if not item:
        raise HTTPException(status_code=404, detail="ml_dataset not found")
    return item

@router.post("/api/ml-datasets/{dataset_id}/export")
async def api_ml_dataset_w171_export_dataset(dataset_id: str, request: Request):
    """Export dataset artifacts"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_dataset(dataset_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_dataset not found")
    return item

@router.post("/api/ml-datasets/{dataset_id}/verify")
async def api_ml_dataset_w171_verify_dataset(dataset_id: str, request: Request):
    """Verify dataset hash integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_dataset(dataset_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_dataset not found")
    return item
