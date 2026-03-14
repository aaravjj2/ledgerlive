"""DigitalOcean Gradient AI endpoints for document processing metrics."""
from __future__ import annotations

from fastapi import APIRouter

from app.services.gradient_ai import get_metrics, extract_document
from app.services.spaces import get_storage_log

router = APIRouter(tags=["gradient-ai"])


@router.get("/api/gradient/metrics")
async def gradient_metrics():
    """Return Gradient AI usage metrics."""
    return get_metrics()


@router.get("/api/gradient/storage-log")
async def storage_log():
    """Return recent document storage operations."""
    return {"operations": get_storage_log()}


@router.post("/api/gradient/extract-demo")
async def extract_demo():
    """Run a demo extraction to verify Gradient AI connectivity."""
    demo_content = b"Demo invoice content for extraction test"
    result = await extract_document(demo_content, "demo-invoice.pdf")
    return result
