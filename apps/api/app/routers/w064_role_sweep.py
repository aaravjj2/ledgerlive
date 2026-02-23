"""Wave 64: Role Sweep E2E Router — Role-based permission sweep: viewer/operator/manager/admin validated with audited denies.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w064_role_sweep import service

router = APIRouter(tags=["Role Sweep E2E"])

@router.get("/api/role-sweeps")
async def api_role_sweep_w64_list_checks(limit: int = 100):
    """List role sweep checks"""
    items = service.list_checks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/role-sweeps", status_code=201)
async def api_role_sweep_w64_run_sweep(request: Request):
    """Run role sweep"""
    data = await request.json()
    item = service.run_sweep(data)
    return item

@router.get("/api/role-sweeps/deny-log")
async def api_role_sweep_w64_deny_log(limit: int = 100):
    """Get audited deny log"""
    items = service.deny_log(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/role-sweeps/matrix")
async def api_role_sweep_w64_role_matrix(limit: int = 100):
    """Get full role permission matrix"""
    items = service.role_matrix(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/role-sweeps/{check_id}")
async def api_role_sweep_w64_get_check(check_id: str):
    """Get check result"""
    item = service.get_check(check_id)
    if not item:
        raise HTTPException(status_code=404, detail="role_sweep not found")
    return item
