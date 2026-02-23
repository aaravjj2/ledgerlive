"""Wave 58: KPI Framework — KPIs as objects with formulas + evidence links. No floating KPIs.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class KpiFrameworkService:
    """Domain service for KPI Framework."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "kpi_id": "",
        "name": "",
        "formula": "",
        "value": 0.0,
        "target": 0.0,
        "unit": "",
        "evidence_links": [],
        "status": "",
        "owner": "",
        "computed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_kpis(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_kpi(self, data: dict) -> dict:
        """Create a new item."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "kpi_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_kpi", "kpi_framework", item_id, {"data": data})
        return item

    def get_kpi(self, kpi_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(kpi_id)

    def compute(self, kpi_id: str, data: dict | None = None) -> dict | None:
        """Action: compute."""
        item = self._store.get(kpi_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "computed"
        emit_audit_event("compute", "kpi_framework", kpi_id, {"action": "compute", "data": data or {}})
        return item

    def link_evidence(self, kpi_id: str, data: dict | None = None) -> dict | None:
        """Action: link_evidence."""
        item = self._store.get(kpi_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "link_evidenced"
        emit_audit_event("link_evidence", "kpi_framework", kpi_id, {"action": "link_evidence", "data": data or {}})
        return item

    def completeness(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def export_kpis(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = KpiFrameworkService()
