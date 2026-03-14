"""Airia Bundle Router — API endpoints for Airia community bundle operations.

PROJECT_ID: LEDGERLIVE

Endpoints:
  GET  /api/airia/status            → bundle hash, template hash, validator status, tools
  POST /api/airia/generate-bundle   → generate/refresh bundle, return hash
  POST /api/airia/validate-bundle   → validate bundle completeness, return PASS/FAIL
  POST /api/airia/verify-bundle     → offline checksum verification, return PASS/FAIL
  GET  /api/airia/compat_report     → deterministic Airia compatibility proof report
"""
from __future__ import annotations

from fastapi import APIRouter

from app.services.airia_bundle import (
    get_bundle_status,
    generate_bundle,
    validate_bundle,
    verify_bundle,
)
from app.services.airia_compat import run_compat_report_cached

router = APIRouter(prefix="/api/airia", tags=["airia"])


@router.get("/status")
async def airia_status() -> dict:
    """Return Airia bundle status: hash, template hash, validator status, tools list."""
    return get_bundle_status()


@router.post("/generate-bundle")
async def airia_generate_bundle() -> dict:
    """Generate / refresh the Airia community bundle. Returns updated hash."""
    return generate_bundle()


@router.post("/validate-bundle")
async def airia_validate_bundle() -> dict:
    """Validate bundle completeness and manifest integrity."""
    return validate_bundle()


@router.post("/verify-bundle")
async def airia_verify_bundle() -> dict:
    """Offline checksum verification of bundle files."""
    return verify_bundle()


@router.get("/compat_report")
async def airia_compat_report() -> dict:
    """Return deterministic Airia platform compatibility proof report."""
    return run_compat_report_cached()
