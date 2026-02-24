"""Race Weekend Stage Model Service — deterministic stage data for Race Control UI.

Maps the 6 race-weekend stages to finance close operations.
Fully offline / deterministic — no external calls.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

# ── Stage Catalogue ───────────────────────────────────────────────────────────
# Each stage maps a racing metaphor to a finance close operation.
# Order is canonical and must never change.

STAGES: list[dict] = [
    {
        "key": "qualifying",
        "ui_label": "Qualifying",
        "description": "Document Intake + OCR kickoff",
        "order": 1,
        "linked_resource": "/documents",
        "approval_required": False,
        "fail_closed": False,
        "evidence_required": True,
        "default_status": "completed",
        "lap_time_ms": 480,
    },
    {
        "key": "formation_lap",
        "ui_label": "Formation Lap",
        "description": "Extraction validation + data quality checks",
        "order": 2,
        "linked_resource": "/reconciliation",
        "approval_required": False,
        "fail_closed": False,
        "evidence_required": True,
        "default_status": "completed",
        "lap_time_ms": 612,
    },
    {
        "key": "pit_stop_1",
        "ui_label": "Pit Stop 1",
        "description": "Reconciliation run + auto-match",
        "order": 3,
        "linked_resource": "/reconciliation",
        "approval_required": False,
        "fail_closed": False,
        "evidence_required": True,
        "default_status": "active",
        "lap_time_ms": 30,
        "pit_stop_time_ms": 30,
    },
    {
        "key": "safety_car",
        "ui_label": "Safety Car",
        "description": "Approval-required gate / fail-closed pause",
        "order": 4,
        "linked_resource": "/review",
        "approval_required": True,
        "fail_closed": True,
        "evidence_required": True,
        "default_status": "pending",
        "lap_time_ms": None,
        "safety_car": True,
    },
    {
        "key": "pit_stop_2",
        "ui_label": "Pit Stop 2",
        "description": "Exception resolution + reviewer decisions",
        "order": 5,
        "linked_resource": "/exceptions",
        "approval_required": True,
        "fail_closed": False,
        "evidence_required": True,
        "default_status": "pending",
        "lap_time_ms": None,
        "pit_stop_time_ms": None,
    },
    {
        "key": "checkered_flag",
        "ui_label": "Checkered Flag",
        "description": "Verified exports (telemetry + court + binder replay equality)",
        "order": 6,
        "linked_resource": "/race-control",
        "approval_required": False,
        "fail_closed": False,
        "evidence_required": True,
        "default_status": "pending",
        "lap_time_ms": None,
    },
]

CRITICAL_PATH = [s["key"] for s in STAGES]


def get_race_weekend_stages() -> dict:
    """Return deterministic race weekend stage data for the Race Control UI timeline."""
    stages = [dict(s) for s in STAGES]

    # Find the first 'pending' stage — that is the current active blocker
    safety_car_active = False
    for stage in stages:
        if stage.get("safety_car") and stage["default_status"] == "pending":
            safety_car_active = True
            break

    # Compute total lap time from completed stages
    completed_lap_ms = sum(
        s["lap_time_ms"]
        for s in stages
        if s["default_status"] == "completed" and s.get("lap_time_ms")
    )

    return {
        "stages": stages,
        "safety_car_active": safety_car_active,
        "critical_path": CRITICAL_PATH,
        "lap_count": len(stages),
        "completed_lap_ms": completed_lap_ms,
        "pit_stop_count": sum(1 for s in stages if "pit_stop" in s["key"]),
    }


def get_stage_keys_ordered() -> list[str]:
    """Return stage keys in canonical order — must never be reordered."""
    return [s["key"] for s in STAGES]
