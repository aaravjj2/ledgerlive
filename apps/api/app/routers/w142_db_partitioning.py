"""Wave 142: DB Partitioning & Indexes Router — Database partitioning and index strategy with explain plan shape guards.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w142_db_partitioning import service

router = APIRouter(tags=["DB Partitioning & Indexes"])

@router.get("/api/db-partitioning")
async def api_db_partitioning_w142_list_partitions(limit: int = 100):
    """List partition configs"""
    items = service.list_partitions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/db-partitioning", status_code=201)
async def api_db_partitioning_w142_create_partition(request: Request):
    """Create partition config"""
    data = await request.json()
    item = service.create_partition(data)
    return item

@router.get("/api/db-partitioning/report")
async def api_db_partitioning_w142_partition_report(limit: int = 100):
    """Get partitioning report"""
    items = service.partition_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/db-partitioning/{partition_id}")
async def api_db_partitioning_w142_get_partition(partition_id: str):
    """Get partition details"""
    item = service.get_partition(partition_id)
    if not item:
        raise HTTPException(status_code=404, detail="db_partitioning not found")
    return item

@router.post("/api/db-partitioning/{partition_id}/analyze")
async def api_db_partitioning_w142_analyze_plan(partition_id: str, request: Request):
    """Analyze explain plan"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.analyze_plan(partition_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="db_partitioning not found")
    return item

@router.post("/api/db-partitioning/{partition_id}/verify")
async def api_db_partitioning_w142_verify_shape(partition_id: str, request: Request):
    """Verify plan shape"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_shape(partition_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="db_partitioning not found")
    return item
