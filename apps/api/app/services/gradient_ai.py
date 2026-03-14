"""DigitalOcean Gradient AI integration for document OCR/extraction.

Uses Gradient AI inference endpoints for GPU-backed document processing.
Falls back to demo mode when no API key is configured.
"""
from __future__ import annotations

import os
import time
import json
import hashlib
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

GRADIENT_AI_API_KEY = os.getenv("GRADIENT_AI_API_KEY", "")
GRADIENT_AI_ENDPOINT = os.getenv("GRADIENT_AI_ENDPOINT", "https://api.gradient.ai/api/v1")

# Metrics tracking
_metrics = {
    "documents_processed": 0,
    "total_latency_ms": 0,
    "total_tokens": 0,
    "errors": 0,
}


def get_metrics() -> dict:
    """Return Gradient AI usage metrics."""
    avg_latency = (
        _metrics["total_latency_ms"] / _metrics["documents_processed"]
        if _metrics["documents_processed"] > 0
        else 0
    )
    return {
        **_metrics,
        "avg_latency_ms": round(avg_latency, 2),
        "api_key_configured": bool(GRADIENT_AI_API_KEY),
    }


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def extract_document(file_bytes: bytes, filename: str, mime_type: str = "application/pdf") -> dict:
    """Extract text and structured data from a document using Gradient AI.

    Returns dict with: text, confidence, metadata, processing_time_ms
    """
    if not GRADIENT_AI_API_KEY:
        # Demo mode — return simulated extraction
        content_hash = hashlib.sha256(file_bytes).hexdigest()[:16]
        _metrics["documents_processed"] += 1
        return {
            "text": f"[Demo] Extracted text from {filename}. Invoice #INV-2026-{content_hash[:6]}. Total: $15,420.00. Tax: $1,234.56. Due: 2026-04-15.",
            "confidence": 0.94,
            "fields": {
                "invoice_number": f"INV-2026-{content_hash[:6]}",
                "total_amount": 15420.00,
                "tax_amount": 1234.56,
                "due_date": "2026-04-15",
                "vendor": "Demo Vendor Corp",
                "currency": "USD",
            },
            "metadata": {
                "filename": filename,
                "content_hash": content_hash,
                "model": "gradient-demo",
                "processing_time_ms": 250,
            },
            "source": "gradient_ai_demo",
        }

    start = time.monotonic()
    async with httpx.AsyncClient(timeout=60.0) as client:
        headers = {
            "Authorization": f"Bearer {GRADIENT_AI_API_KEY}",
            "Content-Type": "application/json",
        }

        import base64
        payload = {
            "model": "gradient-ocr-v1",
            "input": {
                "document": base64.b64encode(file_bytes).decode(),
                "mime_type": mime_type,
                "extraction_mode": "structured",
            }
        }

        resp = await client.post(
            f"{GRADIENT_AI_ENDPOINT}/completions",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        result = resp.json()

    elapsed_ms = round((time.monotonic() - start) * 1000, 2)
    _metrics["documents_processed"] += 1
    _metrics["total_latency_ms"] += elapsed_ms
    _metrics["total_tokens"] += result.get("usage", {}).get("total_tokens", 0)

    return {
        "text": result.get("choices", [{}])[0].get("text", ""),
        "confidence": result.get("confidence", 0.0),
        "fields": result.get("structured_fields", {}),
        "metadata": {
            "filename": filename,
            "model": result.get("model", "gradient-ocr-v1"),
            "processing_time_ms": elapsed_ms,
            "tokens_used": result.get("usage", {}).get("total_tokens", 0),
        },
        "source": "gradient_ai",
    }
