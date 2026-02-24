"""Wave 305: Blueprint-to-Template Compiler v1 Router — Compiles blueprint into Airia template artifacts (offline deterministic).

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w305_blueprint_to_template import service

router = APIRouter(tags=["Blueprint-to-Template Compiler v1"])

@router.get("/api/blueprint-to-template")
async def api_blueprint_to_template_w305_list_compiles(limit: int = 100):
    """List compilations"""
    items = service.list_compiles(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/blueprint-to-template", status_code=201)
async def api_blueprint_to_template_w305_compile_blueprint(request: Request):
    """Compile blueprint to template"""
    data = await request.json()
    item = service.compile_blueprint(data)
    return item

@router.get("/api/blueprint-to-template/report")
async def api_blueprint_to_template_w305_compile_report(limit: int = 100):
    """Get compilation report"""
    items = service.compile_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/blueprint-to-template/{compile_id}")
async def api_blueprint_to_template_w305_get_compile(compile_id: str):
    """Get compilation details"""
    item = service.get_compile(compile_id)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_to_template not found")
    return item

@router.post("/api/blueprint-to-template/{compile_id}/recompile")
async def api_blueprint_to_template_w305_recompile(compile_id: str, request: Request):
    """Recompile blueprint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.recompile(compile_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_to_template not found")
    return item

@router.post("/api/blueprint-to-template/{compile_id}/validate")
async def api_blueprint_to_template_w305_validate_output(compile_id: str, request: Request):
    """Validate compilation output"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_output(compile_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_to_template not found")
    return item
