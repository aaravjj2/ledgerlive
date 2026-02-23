"""Wave 111: Data Lake Export 3.0 Router — Parquet/CSV data lake exports with schema snapshots.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w111_data_lake_export import service

router = APIRouter(tags=["Data Lake Export 3.0"])

@router.get("/api/data-lake-exports")
async def api_data_lake_export_w111_list_exports(limit: int = 100):
    """List data lake exports"""
    items = service.list_exports(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/data-lake-exports", status_code=201)
async def api_data_lake_export_w111_create_export(request: Request):
    """Create data lake export"""
    data = await request.json()
    item = service.create_export(data)
    return item

@router.get("/api/data-lake-exports/history")
async def api_data_lake_export_w111_export_history(limit: int = 100):
    """Get export history"""
    items = service.export_history(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-lake-exports/schema")
async def api_data_lake_export_w111_schema_snapshot(limit: int = 100):
    """Get current schema snapshot"""
    items = service.schema_snapshot(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-lake-exports/{export_id}")
async def api_data_lake_export_w111_get_export(export_id: str):
    """Get export details"""
    item = service.get_export(export_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_lake_export not found")
    return item

@router.post("/api/data-lake-exports/{export_id}/verify")
async def api_data_lake_export_w111_verify_export(export_id: str, request: Request):
    """Verify export integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_export(export_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_lake_export not found")
    return item
