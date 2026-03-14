"""CFO Scenario Pack — Williams Q1 2026 F1 Finance Data.

Deterministic finance dataset for a Williams Racing quarterly close.
All numbers are realistic but fictional. Used by CFO Cockpit and
Ask Race Engineer for grounded, citable responses.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import hashlib
from typing import Any

SCENARIO_ID = "WILLIAMS_Q1_2026"
SCENARIO_VERSION = "2.0.0"

# ── Cost Cap Budget (FIA 2026 rules) ─────────────────────────────
COST_CAP_LIMIT_USD = 135_000_000  # $135M FIA cap
COST_CAP_SPENT_USD = 98_450_000   # spent so far in Q1
COST_CAP_FORECAST_USD = 131_200_000  # projected year-end
COST_CAP_RUNWAY_USD = COST_CAP_LIMIT_USD - COST_CAP_FORECAST_USD  # $3.8M buffer

# ── Invoices & Payables (12 invoices, 4+ currencies: USD GBP EUR JPY) ───────
INVOICES = [
    # Power unit / chassis
    {"id": "INV-2026-001", "vendor": "Mercedes HPP", "category": "power_unit",
     "invoice_number": "MHPP-Q1-001",
     "amount_usd": 12_500_000, "currency": "GBP", "fx_rate": 1.27, "fx_rate_day1": 1.27, "fx_rate_day3": 1.249,
     "amount_local": 9_842_520, "due_date": "2026-03-15", "status": "approved",
     "cap_category": "power_unit", "cost_cap_category": "power_unit_supply",
     "cap_breach_risk": 0.42, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": None},
    # Freight / logistics
    {"id": "INV-2026-002", "vendor": "DHL Logistics", "category": "freight",
     "invoice_number": "DHL-2026-Q1-7832",
     "amount_usd": 2_340_000, "currency": "USD", "fx_rate": 1.0, "fx_rate_day1": 1.0, "fx_rate_day3": 1.0,
     "amount_local": 2_340_000, "due_date": "2026-03-20", "status": "approved",
     "cap_category": "travel", "cost_cap_category": "transportation",
     "cap_breach_risk": 0.08, "logistics_cost_center": "LOG-APAC-001",
     "r_and_d_mapping": None, "recognition_schedule": None},
    # Hospitality (excluded)
    {"id": "INV-2026-003", "vendor": "Hilton Hotels", "category": "hospitality",
     "invoice_number": "HILT-02260315",
     "amount_usd": 890_000, "currency": "EUR", "fx_rate": 1.08, "fx_rate_day1": 1.08, "fx_rate_day3": 1.073,
     "amount_local": 824_074, "due_date": "2026-03-25", "status": "pending_review",
     "cap_category": "other", "cost_cap_category": "excluded_hospitality",
     "cap_breach_risk": 0.0, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": None},
    # R&D / aero parts
    {"id": "INV-2026-004", "vendor": "Williams Advanced Engineering", "category": "r_and_d",
     "invoice_number": "WAE-Q1-2026-088",
     "amount_usd": 4_200_000, "currency": "GBP", "fx_rate": 1.27, "fx_rate_day1": 1.27, "fx_rate_day3": 1.265,
     "amount_local": 3_307_087, "due_date": "2026-04-01", "status": "approved",
     "cap_category": "chassis", "cost_cap_category": "research_development",
     "cap_breach_risk": 0.18, "logistics_cost_center": None, "r_and_d_mapping": "AERO-FW-2026",
     "recognition_schedule": None},
    # Tyres (excluded)
    {"id": "INV-2026-005", "vendor": "Pirelli", "category": "tyres",
     "invoice_number": "PIR-2026-WR-005",
     "amount_usd": 1_850_000, "currency": "EUR", "fx_rate": 1.08, "fx_rate_day1": 1.08, "fx_rate_day3": 1.072,
     "amount_local": 1_712_963, "due_date": "2026-03-30", "status": "approved",
     "cap_category": "other", "cost_cap_category": "excluded_tyres",
     "cap_breach_risk": 0.0, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": None},
    # Travel
    {"id": "INV-2026-006", "vendor": "British Airways", "category": "travel",
     "invoice_number": "BA-CORP-2026-1121",
     "amount_usd": 567_000, "currency": "GBP", "fx_rate": 1.27, "fx_rate_day1": 1.27, "fx_rate_day3": 1.258,
     "amount_local": 446_457, "due_date": "2026-03-18", "status": "flagged",
     "cap_category": "travel", "cost_cap_category": "personnel_travel",
     "cap_breach_risk": 0.05, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": None},
    # Sponsorship revenue
    {"id": "INV-2026-007", "vendor": "Gulf Oil Sponsor", "category": "sponsor_revenue",
     "invoice_number": "GULF-SPNSR-2026-01",
     "amount_usd": -5_000_000, "currency": "USD", "fx_rate": 1.0, "fx_rate_day1": 1.0, "fx_rate_day3": 1.0,
     "amount_local": -5_000_000, "due_date": "2026-04-15", "status": "receivable",
     "cap_category": "other", "cost_cap_category": "excluded_revenue",
     "cap_breach_risk": 0.0, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": {"quarters": ["Q1", "Q2", "Q3", "Q4"], "per_quarter_usd": 1_250_000}},
    {"id": "INV-2026-008", "vendor": "Duracell Sponsor", "category": "sponsor_revenue",
     "invoice_number": "DURACELL-SPNSR-2026-01",
     "amount_usd": -3_200_000, "currency": "USD", "fx_rate": 1.0, "fx_rate_day1": 1.0, "fx_rate_day3": 1.0,
     "amount_local": -3_200_000, "due_date": "2026-04-20", "status": "receivable",
     "cap_category": "other", "cost_cap_category": "excluded_revenue",
     "cap_breach_risk": 0.0, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": {"quarters": ["Q1", "Q2"], "per_quarter_usd": 1_600_000}},
    # Japanese supplier (JPY) — aero parts
    {"id": "INV-2026-009", "vendor": "Honda Manufacturing (Aero)", "category": "aero_parts",
     "invoice_number": "HONDA-AERO-2026-034",
     "amount_usd": 3_850_000, "currency": "JPY", "fx_rate": 149.5, "fx_rate_day1": 149.5, "fx_rate_day3": 151.2,
     "amount_local": 575_575_000, "due_date": "2026-03-28", "status": "approved",
     "cap_category": "chassis", "cost_cap_category": "chassis_components",
     "cap_breach_risk": 0.22, "logistics_cost_center": "LOG-JP-AERO",
     "r_and_d_mapping": "AERO-FLOOR-2026", "recognition_schedule": None},
    # Freight from Japan (JPY)
    {"id": "INV-2026-010", "vendor": "Yamato Transport", "category": "freight",
     "invoice_number": "YTC-FRT-2026-112",
     "amount_usd": 780_000, "currency": "JPY", "fx_rate": 149.5, "fx_rate_day1": 149.5, "fx_rate_day3": 151.0,
     "amount_local": 116_610_000, "due_date": "2026-03-22", "status": "approved",
     "cap_category": "travel", "cost_cap_category": "transportation",
     "cap_breach_risk": 0.03, "logistics_cost_center": "LOG-JP-FRT-001",
     "r_and_d_mapping": None, "recognition_schedule": None},
    # Personnel — EUR
    {"id": "INV-2026-011", "vendor": "AMS Technical Staffing", "category": "personnel",
     "invoice_number": "AMS-PERS-2026-Q1",
     "amount_usd": 2_100_000, "currency": "EUR", "fx_rate": 1.08, "fx_rate_day1": 1.08, "fx_rate_day3": 1.075,
     "amount_local": 1_944_444, "due_date": "2026-03-31", "status": "approved",
     "cap_category": "personnel", "cost_cap_category": "personnel_costs",
     "cap_breach_risk": 0.12, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": None},
    # Sponsorship receivable (EUR) + revenue_recognition
    {"id": "INV-2026-012", "vendor": "ORLEN Group Sponsorship", "category": "sponsor_revenue",
     "invoice_number": "ORLEN-SPNSR-2026-Q1",
     "amount_usd": -4_500_000, "currency": "EUR", "fx_rate": 1.08, "fx_rate_day1": 1.08, "fx_rate_day3": 1.072,
     "amount_local": -4_166_667, "due_date": "2026-04-01", "status": "receivable",
     "cap_category": "other", "cost_cap_category": "excluded_revenue",
     "cap_breach_risk": 0.0, "logistics_cost_center": None, "r_and_d_mapping": None,
     "recognition_schedule": {"quarters": ["Q1", "Q2", "Q3", "Q4"], "per_quarter_usd": 1_125_000}},
]

# ── Exception Impact Metrics ──────────────────────────────────────
EXCEPTIONS_BEFORE = [
    {"id": "EXC-F1-001", "description": "Duplicate freight payment to DHL",
     "amount_usd": 78_000, "risk": "overpayment", "status": "open"},
    {"id": "EXC-F1-002", "description": "FX variance on Mercedes HPP invoice",
     "amount_usd": 142_500, "risk": "cost_cap_breach", "status": "open"},
    {"id": "EXC-F1-003", "description": "Missing PO for Hilton hospitality",
     "amount_usd": 45_000, "risk": "compliance", "status": "open"},
]
EXCEPTIONS_AFTER = [
    {"id": "EXC-F1-001", "description": "Duplicate freight payment to DHL",
     "amount_usd": 78_000, "risk": "overpayment", "status": "auto_resolved",
     "resolution": "Agent matched duplicate invoice numbers, flagged for recovery. Saves $78K."},
    {"id": "EXC-F1-002", "description": "FX variance on Mercedes HPP invoice",
     "amount_usd": 142_500, "risk": "cost_cap_breach", "status": "escalated_to_cfo",
     "resolution": "Agent computed FX impact on cost cap; variance pushes forecast to $131.34M. "
                   "Recommended hedge action to treasury. Avoids $142.5K cost cap risk."},
    {"id": "EXC-F1-003", "description": "Missing PO for Hilton hospitality",
     "amount_usd": 45_000, "risk": "compliance", "status": "auto_resolved",
     "resolution": "Hospitality is excluded from cost cap (FIA Art. 4.1b). "
                   "Agent auto-classified and approved. Saves 2 hours of manual review."},
]

# ── Close Velocity (lap times per stage) ──────────────────────────
CLOSE_STAGES = [
    {"stage": "Pit Stop: Ingest", "manual_hours": 16, "agent_hours": 0.5,
     "speedup_x": 32, "status": "completed"},
    {"stage": "Qualifying: Reconcile", "manual_hours": 24, "agent_hours": 1.2,
     "speedup_x": 20, "status": "completed"},
    {"stage": "Safety Car: Triage", "manual_hours": 12, "agent_hours": 0.3,
     "speedup_x": 40, "status": "completed"},
    {"stage": "Race: Review", "manual_hours": 8, "agent_hours": 2.0,
     "speedup_x": 4, "status": "in_progress"},
    {"stage": "Podium: Binder", "manual_hours": 6, "agent_hours": 0.1,
     "speedup_x": 60, "status": "pending"},
]

# ── CFO Summary Metrics ──────────────────────────────────────────
def get_cfo_metrics() -> dict[str, Any]:
    """Compute deterministic CFO cockpit metrics from scenario data."""
    total_payable = sum(i["amount_usd"] for i in INVOICES if i["amount_usd"] > 0)
    total_receivable = abs(sum(i["amount_usd"] for i in INVOICES if i["amount_usd"] < 0))
    exception_impact_before = sum(e["amount_usd"] for e in EXCEPTIONS_BEFORE)
    exception_impact_after = sum(e["amount_usd"] for e in EXCEPTIONS_AFTER if e["status"] != "auto_resolved")
    time_saved_hours = sum(s["manual_hours"] - s["agent_hours"] for s in CLOSE_STAGES)
    manual_total = sum(s["manual_hours"] for s in CLOSE_STAGES)
    agent_total = sum(s["agent_hours"] for s in CLOSE_STAGES)

    return {
        "scenario_id": SCENARIO_ID,
        "scenario_version": SCENARIO_VERSION,
        "cost_cap": {
            "limit_usd": COST_CAP_LIMIT_USD,
            "spent_usd": COST_CAP_SPENT_USD,
            "forecast_usd": COST_CAP_FORECAST_USD,
            "runway_usd": COST_CAP_RUNWAY_USD,
            "runway_pct": round(COST_CAP_RUNWAY_USD / COST_CAP_LIMIT_USD * 100, 1),
            "risk_level": "medium" if COST_CAP_RUNWAY_USD < 5_000_000 else "low",
        },
        "exception_impact": {
            "before_usd": exception_impact_before,
            "after_usd": exception_impact_after,
            "saved_usd": exception_impact_before - exception_impact_after,
            "auto_resolved_count": sum(1 for e in EXCEPTIONS_AFTER if e["status"] == "auto_resolved"),
            "escalated_count": sum(1 for e in EXCEPTIONS_AFTER if "escalated" in e["status"]),
        },
        "close_velocity": {
            "manual_hours": manual_total,
            "agent_hours": agent_total,
            "time_saved_hours": time_saved_hours,
            "speedup_x": round(manual_total / max(agent_total, 0.1), 1),
            "stages": CLOSE_STAGES,
        },
        "financials": {
            "total_payable_usd": total_payable,
            "total_receivable_usd": total_receivable,
            "net_position_usd": total_receivable - total_payable,
            "invoices_count": len(INVOICES),
            "currencies": list(set(i["currency"] for i in INVOICES)),
        },
        "cfo_summary": (
            f"After this close cycle: cost cap runway ${COST_CAP_RUNWAY_USD:,.0f} "
            f"({round(COST_CAP_RUNWAY_USD / COST_CAP_LIMIT_USD * 100, 1)}% buffer), "
            f"risk flags 1 (FX variance on power unit), "
            f"time saved {time_saved_hours:.1f} hours vs manual close "
            f"({round(manual_total / max(agent_total, 0.1), 1)}x speedup). "
            f"Agent auto-resolved 2/3 exceptions saving $123K."
        ),
        # ── B5: Runway by category, Cash ladder, Vendor concentration ──────────
        "runway_by_category": {
            "chassis":      {"spent_usd": 8_050_000,  "budget_usd": 18_000_000, "runway_usd": 9_950_000},
            "power_unit":   {"spent_usd": 12_500_000, "budget_usd": 17_000_000, "runway_usd": 4_500_000},
            "personnel":    {"spent_usd": 42_000_000, "budget_usd": 55_000_000, "runway_usd": 13_000_000},
            "travel":       {"spent_usd": 2_907_000,  "budget_usd": 4_000_000,  "runway_usd": 1_093_000},
            "other":        {"spent_usd": 32_993_000, "budget_usd": 41_000_000, "runway_usd": 8_007_000},
        },
        "cash_ladder": {
            "7_day_usd":  sum(i["amount_usd"] for i in INVOICES if i["amount_usd"] > 0
                              and i["due_date"] <= "2026-03-22"),
            "14_day_usd": sum(i["amount_usd"] for i in INVOICES if i["amount_usd"] > 0
                              and i["due_date"] <= "2026-03-29"),
            "30_day_usd": sum(i["amount_usd"] for i in INVOICES if i["amount_usd"] > 0
                              and i["due_date"] <= "2026-04-25"),
            "receivables_30_day_usd": abs(sum(i["amount_usd"] for i in INVOICES
                                              if i["amount_usd"] < 0)),
        },
        "vendor_concentration": {
            "top_vendors": [
                {"vendor": "Mercedes HPP",               "exposure_usd": 12_500_000, "pct_of_cap": 9.3},
                {"vendor": "Williams Advanced Engineering","exposure_usd": 4_200_000,  "pct_of_cap": 3.1},
                {"vendor": "AMS Technical Staffing",      "exposure_usd": 2_100_000,  "pct_of_cap": 1.6},
                {"vendor": "DHL Logistics",               "exposure_usd": 2_340_000,  "pct_of_cap": 1.7},
                {"vendor": "Honda Manufacturing (Aero)",  "exposure_usd": 3_850_000,  "pct_of_cap": 2.9},
            ],
            "single_vendor_cap_risk": "Mercedes HPP at 9.3% of cap is the highest concentration risk",
        },
        # ── B6: Forecast delta after close adjustments ────────────────────────
        "forecast_delta": {
            "original_forecast_usd":  132_500_000,
            "adjusted_forecast_usd":  131_200_000,
            "delta_amount_usd":       -1_300_000,
            "delta_pct":             round(-1_300_000 / 132_500_000 * 100, 2),
            "adjustment_reason":      "Auto-resolved duplicate freight ($78K) + hospitality re-class ($45K) + FX hedge ($1.177M)",
            "cap_breach_risk_after":  "Low — runway $3.8M after adjustments",
        },
    }


def get_scenario_pack() -> dict[str, Any]:
    """Return the full Williams Q1 2026 scenario pack."""
    return {
        "scenario_id": SCENARIO_ID,
        "version": SCENARIO_VERSION,
        "team": "Williams Racing",
        "period": "Q1 2026",
        "cost_cap_limit_usd": COST_CAP_LIMIT_USD,
        "invoices": INVOICES,
        "exceptions_before": EXCEPTIONS_BEFORE,
        "exceptions_after": EXCEPTIONS_AFTER,
        "close_stages": CLOSE_STAGES,
        "metrics": get_cfo_metrics(),
        "checksum": hashlib.sha256(
            f"{SCENARIO_ID}-{SCENARIO_VERSION}-{len(INVOICES)}".encode()
        ).hexdigest()[:16],
    }


# ── Ask Race Engineer — deterministic intent parsing ─────────────
ENGINEER_RESPONSES: dict[str, dict[str, Any]] = {
    "blocking": {
        "intent": "what_is_blocking",
        "answer": (
            "Two items are blocking the close:\n"
            "1. EXC-F1-002: FX variance on Mercedes HPP invoice ($142,500 risk). "
            "Escalated to CFO for hedge decision. [Dossier: /api/exceptions/exc-0002]\n"
            "2. Review Queue: 2 pending approvals from finance controller and treasury. "
            "[Queue: /api/reviews]\n"
            "Recommended action: approve the hospitality auto-classification, "
            "then address the FX hedge recommendation."
        ),
        "citations": ["exc-0002", "rev-0001", "rev-0002"],
        "action": None,
    },
    "cost_cap": {
        "intent": "cost_cap_runway",
        "answer": (
            f"Cost cap runway: ${COST_CAP_RUNWAY_USD:,.0f} "
            f"({round(COST_CAP_RUNWAY_USD / COST_CAP_LIMIT_USD * 100, 1)}% buffer).\n"
            f"Current spend: ${COST_CAP_SPENT_USD:,.0f} of ${COST_CAP_LIMIT_USD:,.0f} limit.\n"
            f"Year-end forecast: ${COST_CAP_FORECAST_USD:,.0f}.\n"
            f"Risk: Medium — FX variance on power unit invoice could reduce runway by $142.5K.\n"
            f"[Source: ScenarioPack {SCENARIO_ID} / Cost Cap Module]"
        ),
        "citations": [SCENARIO_ID, "INV-2026-001"],
        "action": None,
    },
    "highest_risk": {
        "intent": "highest_risk_vendor",
        "answer": (
            "Highest risk vendor: Mercedes HPP (power unit supplier).\n"
            "Reason: INV-2026-001 ($12.5M) has a $142,500 FX variance that "
            "could impact cost cap compliance. The invoice is denominated in GBP "
            "with a 1.27 exchange rate; a 1% adverse move adds $125K to cost cap spend.\n"
            "Second highest: DHL Logistics — duplicate payment of $78K detected and "
            "auto-recovered by the agent.\n"
            "[Evidence: /api/cfo/scenario, /api/exceptions]"
        ),
        "citations": ["INV-2026-001", "EXC-F1-002", "INV-2026-002", "EXC-F1-001"],
        "action": None,
    },
    "approve_next": {
        "intent": "what_to_approve",
        "answer": (
            "Recommended approval order:\n"
            "1. REV-0001: $500 variance (amount mismatch) — low risk, fast approval. "
            "Clearing this unblocks the reconciliation lane.\n"
            "2. REV-0002: $7,800 duplicate payment — critical but recovery already initiated. "
            "Approve to advance treasury recovery workflow.\n"
            "After both approvals, the close can advance to Podium (Evidence Binder) stage.\n"
            "[Queue: /api/reviews]"
        ),
        "citations": ["rev-0001", "rev-0002", "wf-0001"],
        "action": {"type": "navigate", "target": "/api/reviews"},
    },
    "exception_why": {
        "intent": "explain_exception",
        "answer": (
            "Exception EXC-0001 was flagged because:\n"
            "- Accrual reversal posted 2 days after period close ($3,200)\n"
            "- AI triage model (ledgerlive-triage-v1) classified as 'auto_resolvable' "
            "with 92% confidence\n"
            "- Reason: Normal timing pattern — accrual reversed in next period\n"
            "- Impact on cost cap: None (below materiality threshold)\n"
            "[Dossier: /api/exceptions/exc-0001, Model: ledgerlive-triage-v1]"
        ),
        "citations": ["exc-0001", "ledgerlive-triage-v1"],
        "action": None,
    },
    "court_pack": {
        "intent": "generate_court_pack",
        "answer": (
            "Court pack generation initiated.\n"
            "Contents:\n"
            "- 5 ingested documents with SHA-256 hashes\n"
            "- 3 reconciliation results with match scores\n"
            "- 3 exception triage reports with AI reasoning\n"
            "- 2 workflow traces with step-by-step decisions\n"
            "- Audit trail: all tool calls with timestamps\n"
            "The pack is sealed with a deterministic checksum for steward verification.\n"
            "[Endpoint: /api/ops/export/court-pack]"
        ),
        "citations": ["wf-0001", "wf-0002"],
        "action": {"type": "api_call", "method": "POST", "target": "/api/ops/export/court-pack"},
    },
}

# Intent keyword mapping
_INTENT_KEYWORDS = {
    "blocking": ["blocking", "block", "stuck", "what's blocking", "blocker"],
    "cost_cap": ["cost cap", "runway", "budget", "cap runway", "how much left"],
    "highest_risk": ["highest risk", "riskiest", "risk vendor", "which vendor"],
    "approve_next": ["approve", "approval", "what should", "what next", "recommend"],
    "exception_why": ["why", "flagged", "exception", "explain", "show me why"],
    "court_pack": ["court pack", "generate", "evidence pack", "steward", "court"],
}


def parse_intent(question: str) -> str:
    """Deterministic intent parsing — no LLM needed in DEMO mode."""
    q = question.lower().strip()
    best_match = "blocking"  # default
    best_score = 0
    for intent, keywords in _INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q)
        if score > best_score:
            best_score = score
            best_match = intent
    return best_match


def ask_race_engineer(question: str) -> dict[str, Any]:
    """Process a question through deterministic intent parsing."""
    intent = parse_intent(question)
    response = ENGINEER_RESPONSES.get(intent, ENGINEER_RESPONSES["blocking"])
    return {
        "question": question,
        "intent": response["intent"],
        "answer": response["answer"],
        "citations": response["citations"],
        "action": response.get("action"),
        "model": "deterministic-intent-v1",
        "scenario": SCENARIO_ID,
    }
