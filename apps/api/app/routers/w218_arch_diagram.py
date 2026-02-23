"""Wave 218: Auto Architecture Diagram Generator v1 Router — Generate architecture diagram from routers registry, tool registry, workflow DAG, storage components. Output dot/mermaid source deterministically.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w218_arch_diagram import service

router = APIRouter(tags=["Auto Architecture Diagram Generator v1"])

@router.get("/api/arch-diagrams")
async def api_arch_diagram_w218_list_diagrams(limit: int = 100):
    """List architecture diagrams"""
    items = service.list_diagrams(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/arch-diagrams", status_code=201)
async def api_arch_diagram_w218_generate_diagram(request: Request):
    """Generate architecture diagram"""
    data = await request.json()
    item = service.generate_diagram(data)
    return item

@router.get("/api/arch-diagrams/report")
async def api_arch_diagram_w218_diagram_report(limit: int = 100):
    """Get diagram generation report"""
    items = service.diagram_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/arch-diagrams/{diagram_id}")
async def api_arch_diagram_w218_get_diagram(diagram_id: str):
    """Get diagram details"""
    item = service.get_diagram(diagram_id)
    if not item:
        raise HTTPException(status_code=404, detail="arch_diagram not found")
    return item

@router.post("/api/arch-diagrams/{diagram_id}/export")
async def api_arch_diagram_w218_export_diagram(diagram_id: str, request: Request):
    """Export diagram artifact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_diagram(diagram_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="arch_diagram not found")
    return item

@router.post("/api/arch-diagrams/{diagram_id}/validate")
async def api_arch_diagram_w218_validate_diagram(diagram_id: str, request: Request):
    """Validate diagram source"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_diagram(diagram_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="arch_diagram not found")
    return item
