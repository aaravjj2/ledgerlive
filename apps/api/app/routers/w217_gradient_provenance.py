"""Wave 217: Gradient Provenance Capture v1 Router — When Gradient live enabled, capture provenance: job spec hash, artifact hash, endpoint hash. DEMO generates deterministic provenance placeholder.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w217_gradient_provenance import service

router = APIRouter(tags=["Gradient Provenance Capture v1"])

@router.get("/api/gradient-provenance")
async def api_gradient_provenance_w217_list_provenance(limit: int = 100):
    """List provenance records"""
    items = service.list_provenance(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/gradient-provenance", status_code=201)
async def api_gradient_provenance_w217_capture_provenance(request: Request):
    """Capture gradient provenance"""
    data = await request.json()
    item = service.capture_provenance(data)
    return item

@router.get("/api/gradient-provenance/report")
async def api_gradient_provenance_w217_provenance_report(limit: int = 100):
    """Get provenance report"""
    items = service.provenance_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/gradient-provenance/{provenance_id}")
async def api_gradient_provenance_w217_get_provenance(provenance_id: str):
    """Get provenance details"""
    item = service.get_provenance(provenance_id)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_provenance not found")
    return item

@router.post("/api/gradient-provenance/{provenance_id}/placeholder")
async def api_gradient_provenance_w217_generate_placeholder(provenance_id: str, request: Request):
    """Generate DEMO placeholder"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_placeholder(provenance_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_provenance not found")
    return item

@router.post("/api/gradient-provenance/{provenance_id}/validate")
async def api_gradient_provenance_w217_validate_provenance(provenance_id: str, request: Request):
    """Validate provenance schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_provenance(provenance_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="gradient_provenance not found")
    return item
