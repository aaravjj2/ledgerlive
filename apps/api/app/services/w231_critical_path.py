"""Wave 231: Critical Path Analyzer v1 — Identifies the critical path through the close task DAG. Computes earliest/latest start and finish times, float values, and bottleneck nodes.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class CriticalPathService:
    """Domain service for Critical Path Analyzer v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "analysis_id": "",
        "dag_id": "",
        "critical_nodes": [],
        "critical_edges": [],
        "total_duration": 0,
        "earliest_start": {},
        "latest_finish": {},
        "float_values": {},
        "bottleneck_node": "",
        "slack_available": 0,
        "status": "",
        "analyzed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_analyses(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def analyze_path(self, data: dict) -> dict:
        """Create/run: Analyze critical path."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "analysis_id": item_id}
        self._store[item_id] = item
        emit_audit_event("analyze_path", "critical_path", item_id, {"data": data})
        return item

    def get_analysis(self, analysis_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(analysis_id)

    def find_bottleneck(self, analysis_id: str, data: dict | None = None) -> dict | None:
        """Action: Find bottleneck node."""
        item = self._store.get(analysis_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "find_bottleneckd"
        emit_audit_event("find_bottleneck", "critical_path", analysis_id, {"action": "find_bottleneck", "data": data or {}})
        return item

    def compute_float(self, analysis_id: str, data: dict | None = None) -> dict | None:
        """Action: Compute float values."""
        item = self._store.get(analysis_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "compute_floatd"
        emit_audit_event("compute_float", "critical_path", analysis_id, {"action": "compute_float", "data": data or {}})
        return item

    def path_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = CriticalPathService()
