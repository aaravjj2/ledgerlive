"""CFO Cockpit Router — Real-time F1 finance metrics for Williams Racing.

Provides cost cap runway, exception dollar impact, and close velocity
metrics. All data comes from the deterministic CFO scenario pack.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["CFO Cockpit"])


@router.get("/api/cfo/cockpit")
async def get_cfo_cockpit():
    """CFO Cockpit — live finance metrics for the Williams F1 CFO."""
    from app.services.cfo_scenario import get_cfo_metrics
    from app.services.w07_exception import service as exc_svc
    from app.services.w06_reconciliation import service as recon_svc
    from app.services.w13_workflow import service as wf_svc

    metrics = get_cfo_metrics()

    # Overlay live data from current state
    exceptions = exc_svc.list()
    recons = recon_svc.list()
    workflows = wf_svc.list()

    metrics["live_overlay"] = {
        "exceptions_open": sum(1 for e in exceptions if e.get("status") in ("open", "escalated")),
        "exceptions_resolved": sum(1 for e in exceptions if e.get("status") == "resolved"),
        "reconciliations_approved": sum(1 for r in recons if r.get("status") == "approved"),
        "workflows_active": sum(1 for w in workflows if w.get("status") == "in_progress"),
        "workflows_completed": sum(1 for w in workflows if w.get("status") == "completed"),
    }

    return metrics


@router.get("/api/cfo/scenario")
async def get_scenario():
    """Full Williams Q1 2026 scenario pack with invoices, exceptions, and stages."""
    from app.services.cfo_scenario import get_scenario_pack
    return get_scenario_pack()


@router.get("/api/cfo/story-mode")
async def get_story_mode():
    """CFO Story Mode — guided walkthrough steps for the demo."""
    from app.services.cfo_scenario import get_cfo_metrics, COST_CAP_RUNWAY_USD, COST_CAP_LIMIT_USD
    metrics = get_cfo_metrics()

    return {
        "enabled": True,
        "title": "Williams F1 CFO Close Walkthrough",
        "subtitle": "Experience a quarterly close like the Williams pit wall runs a race",
        "steps": [
            {
                "step": 1,
                "title": "Pit Stop: Ingest Documents",
                "description": "5 real invoices from Mercedes HPP, DHL, Pirelli, and sponsors land in the document store. OCR extracts amounts, dates, and vendor details.",
                "panel": "documents",
                "action_label": "Show me",
                "route": "/documents",
                "testid": "cfo-story-step-1",
            },
            {
                "step": 2,
                "title": "Qualifying: Reconcile Accounts",
                "description": "Agent matches bank feeds to GL, subledger to GL, and vendor statements to AP. 314/333 entries matched automatically (94.3% hit rate).",
                "panel": "reconciliation",
                "action_label": "Show me",
                "route": "/reconciliation",
                "testid": "cfo-story-step-2",
            },
            {
                "step": 3,
                "title": "Safety Car: Triage Exceptions",
                "description": "3 exceptions flagged — duplicate freight payment ($78K), FX variance on power unit ($142.5K), missing PO for hospitality ($45K). AI triages each with confidence scores.",
                "panel": "exceptions",
                "action_label": "Show me",
                "route": "/exceptions",
                "testid": "cfo-story-step-3",
            },
            {
                "step": 4,
                "title": "DRS Zone: Auto-Resolve",
                "description": "Agent auto-resolves 2/3 exceptions: recovers duplicate payment, approves excluded hospitality. Only the FX variance escalates to CFO. This reduces exception impact by $123K and saves 2 hours.",
                "panel": "exceptions",
                "action_label": "Show me",
                "route": "/exceptions",
                "testid": "cfo-story-step-4",
            },
            {
                "step": 5,
                "title": "Pit Wall: Approve & Decide",
                "description": f"CFO reviews the FX hedge recommendation. Cost cap runway: ${COST_CAP_RUNWAY_USD:,.0f} ({round(COST_CAP_RUNWAY_USD / COST_CAP_LIMIT_USD * 100, 1)}% buffer). Two approvals pending in the review queue.",
                "panel": "review",
                "action_label": "Show me",
                "route": "/review-queue",
                "testid": "cfo-story-step-5",
            },
            {
                "step": 6,
                "title": "Podium: Seal the Evidence",
                "description": "Court pack generated with SHA-256 integrity seals. Telemetry pack captures every tool call. The close is audit-ready and steward-certified.",
                "panel": "race-control",
                "action_label": "Show me",
                "route": "/race-control",
                "testid": "cfo-story-step-6",
            },
        ],
        "cfo_summary_card": metrics["cfo_summary"],
    }
