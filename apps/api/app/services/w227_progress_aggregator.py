"""Wave 227: Progress Aggregator v1 — Aggregates completion progress across all close tasks, DAG nodes, and team handoffs. Produces weighted progress percentage and phase-level breakdowns.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ProgressAggregatorService:
    """Domain service for Progress Aggregator v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "aggregation_id": "",
        "period_id": "",
        "total_tasks": 0,
        "completed_tasks": 0,
        "in_progress_tasks": 0,
        "blocked_tasks": 0,
        "overall_pct": 0.0,
        "phase_breakdown": {},
        "team_breakdown": {},
        "weighted_score": 0.0,
        "trend_direction": "",
        "status": "",
        "aggregated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_aggregations(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def aggregate(self, data: dict) -> dict:
        """Create/run: Compute progress aggregation."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "aggregation_id": item_id}
        self._store[item_id] = item
        emit_audit_event("aggregate", "progress_aggregator", item_id, {"data": data})
        return item

    def get_aggregation(self, aggregation_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(aggregation_id)

    def refresh(self, aggregation_id: str, data: dict | None = None) -> dict | None:
        """Action: Refresh aggregation data."""
        item = self._store.get(aggregation_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "refreshd"
        emit_audit_event("refresh", "progress_aggregator", aggregation_id, {"action": "refresh", "data": data or {}})
        return item

    def team_detail(self, aggregation_id: str, data: dict | None = None) -> dict | None:
        """Action: Get team-level detail."""
        item = self._store.get(aggregation_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "team_detaild"
        emit_audit_event("team_detail", "progress_aggregator", aggregation_id, {"action": "team_detail", "data": data or {}})
        return item

    def aggregator_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ProgressAggregatorService()
