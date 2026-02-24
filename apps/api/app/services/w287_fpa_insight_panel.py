"""Wave 287: FP&A Insight Panel v1 — Budgets, forecast, and scenario deltas surfaced in Race Control as telemetry. Deterministic variance analysis.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class FpaInsightPanelService:
    """Domain service for FP&A Insight Panel v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "insight_id": "",
        "period_ref": "",
        "budget_data": {},
        "forecast_data": {},
        "scenario_deltas": [],
        "variance_analysis": {},
        "key_drivers": [],
        "telemetry_ref": "",
        "rc_display_config": {},
        "deterministic": True,
        "confidence_level": 0.0,
        "status": "",
        "analyzed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_insights(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_insight(self, data: dict) -> dict:
        """Create/run: Create FP&A insight."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "insight_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_insight", "fpa_insight_panel", item_id, {"data": data})
        return item

    def get_insight(self, insight_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(insight_id)

    def analyze_variance(self, insight_id: str, data: dict | None = None) -> dict | None:
        """Action: Analyze variance."""
        item = self._store.get(insight_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "analyze_varianced"
        emit_audit_event("analyze_variance", "fpa_insight_panel", insight_id, {"action": "analyze_variance", "data": data or {}})
        return item

    def run_scenario(self, insight_id: str, data: dict | None = None) -> dict | None:
        """Action: Run scenario analysis."""
        item = self._store.get(insight_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "run_scenariod"
        emit_audit_event("run_scenario", "fpa_insight_panel", insight_id, {"action": "run_scenario", "data": data or {}})
        return item

    def insight_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = FpaInsightPanelService()
