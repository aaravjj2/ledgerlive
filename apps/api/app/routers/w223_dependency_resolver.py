"""Wave 223: Dependency Resolver v1 Router — Resolves task dependencies from DAG, determines execution readiness, detects circular references, and produces parallelizable task batches for close execution.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w223_dependency_resolver import service

router = APIRouter(tags=["Dependency Resolver v1"])

@router.get("/api/dependency-resolver")
async def api_dependency_resolver_w223_list_resolutions(limit: int = 100):
    """List dependency resolutions"""
    items = service.list_resolutions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/dependency-resolver", status_code=201)
async def api_dependency_resolver_w223_resolve_deps(request: Request):
    """Resolve dependencies from DAG"""
    data = await request.json()
    item = service.resolve_deps(data)
    return item

@router.get("/api/dependency-resolver/report")
async def api_dependency_resolver_w223_resolver_report(limit: int = 100):
    """Get dependency resolver report"""
    items = service.resolver_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/dependency-resolver/{resolver_id}")
async def api_dependency_resolver_w223_get_resolution(resolver_id: str):
    """Get resolution details"""
    item = service.get_resolution(resolver_id)
    if not item:
        raise HTTPException(status_code=404, detail="dependency_resolver not found")
    return item

@router.post("/api/dependency-resolver/{resolver_id}/circular")
async def api_dependency_resolver_w223_detect_circular(resolver_id: str, request: Request):
    """Detect circular references"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.detect_circular(resolver_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="dependency_resolver not found")
    return item

@router.post("/api/dependency-resolver/{resolver_id}/ready")
async def api_dependency_resolver_w223_check_ready(resolver_id: str, request: Request):
    """Check which tasks are ready"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_ready(resolver_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="dependency_resolver not found")
    return item
