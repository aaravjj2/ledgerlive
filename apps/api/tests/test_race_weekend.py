"""test_race_weekend.py — Race Weekend Stage Model assertions.

Validates:
- Stage mapping table contains all 6 canonical stages
- Stage order is fixed and never changes
- Stage keys are unique
- Safety car stage has approval_required=True and fail_closed=True
- Service returns correct shape

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import pytest

from app.services.race_weekend import STAGES, CRITICAL_PATH, get_race_weekend_stages, get_stage_keys_ordered

# Canonical keys in canonical order — must never be reordered
CANONICAL_KEYS = [
    "qualifying",
    "formation_lap",
    "pit_stop_1",
    "safety_car",
    "pit_stop_2",
    "checkered_flag",
]

# UI labels in order
CANONICAL_LABELS = [
    "Qualifying",
    "Formation Lap",
    "Pit Stop 1",
    "Safety Car",
    "Pit Stop 2",
    "Checkered Flag",
]


# ── Stage Count + Keys ────────────────────────────────────────────────────────

def test_stage_count():
    assert len(STAGES) == 6, "Must have exactly 6 race weekend stages"


@pytest.mark.parametrize("key", CANONICAL_KEYS)
def test_stage_key_present(key: str):
    keys = [s["key"] for s in STAGES]
    assert key in keys, f"Stage key missing: {key!r}"


def test_stage_keys_unique():
    keys = [s["key"] for s in STAGES]
    assert len(keys) == len(set(keys)), "Stage keys must be unique"


# ── Order is canonical and immutable ─────────────────────────────────────────

def test_stage_order_immutable():
    """Critical: stage ordering must match the canonical spec exactly."""
    keys = get_stage_keys_ordered()
    assert keys == CANONICAL_KEYS, (
        f"Stage order changed!\nExpected: {CANONICAL_KEYS}\nGot:      {keys}"
    )


def test_critical_path_matches():
    assert CRITICAL_PATH == CANONICAL_KEYS, "CRITICAL_PATH must equal CANONICAL_KEYS"


def test_stage_orders_ascending():
    orders = [s["order"] for s in STAGES]
    assert orders == sorted(orders), "Stage 'order' fields must be ascending"


# ── Safety Car stage ─────────────────────────────────────────────────────────

def test_safety_car_approval_required():
    sc = next(s for s in STAGES if s["key"] == "safety_car")
    assert sc["approval_required"] is True, "safety_car stage must have approval_required=True"


def test_safety_car_fail_closed():
    sc = next(s for s in STAGES if s["key"] == "safety_car")
    assert sc["fail_closed"] is True, "safety_car stage must have fail_closed=True"


def test_safety_car_has_safety_car_flag():
    sc = next(s for s in STAGES if s["key"] == "safety_car")
    assert sc.get("safety_car") is True


# ── Pit stop stages ───────────────────────────────────────────────────────────

def test_pit_stop_stages_count():
    pit_stages = [s for s in STAGES if "pit_stop" in s["key"]]
    assert len(pit_stages) == 2, "Must have 2 pit stop stages"


def test_pit_stop_1_has_lap_time():
    ps1 = next(s for s in STAGES if s["key"] == "pit_stop_1")
    assert ps1.get("lap_time_ms") is not None, "pit_stop_1 must have lap_time_ms"


# ── Service response shape ────────────────────────────────────────────────────

def test_get_race_weekend_stages_shape():
    result = get_race_weekend_stages()
    assert "stages" in result
    assert "safety_car_active" in result
    assert "critical_path" in result
    assert "lap_count" in result
    assert "completed_lap_ms" in result
    assert "pit_stop_count" in result


def test_get_race_weekend_stages_count():
    result = get_race_weekend_stages()
    assert len(result["stages"]) == 6


def test_get_race_weekend_stages_critical_path():
    result = get_race_weekend_stages()
    assert result["critical_path"] == CANONICAL_KEYS


def test_get_race_weekend_stages_pit_stop_count():
    result = get_race_weekend_stages()
    assert result["pit_stop_count"] == 2


def test_get_race_weekend_stages_deterministic():
    """Running twice must return identical results."""
    r1 = get_race_weekend_stages()
    r2 = get_race_weekend_stages()
    assert r1 == r2, "get_race_weekend_stages() must be deterministic"


# ── UI labels – all required labels present ──────────────────────────────────

@pytest.mark.parametrize("label", CANONICAL_LABELS)
def test_stage_ui_label(label: str):
    labels = [s["ui_label"] for s in STAGES]
    assert label in labels, f"Stage ui_label missing: {label!r}"


# ── Linked resources ─────────────────────────────────────────────────────────

def test_stages_have_linked_resources():
    for s in STAGES:
        assert s.get("linked_resource"), f"Stage {s['key']} must have linked_resource"


# ── Evidence required ─────────────────────────────────────────────────────────

def test_all_stages_evidence_required():
    for s in STAGES:
        assert s.get("evidence_required") is True, (
            f"Stage {s['key']} must have evidence_required=True"
        )
