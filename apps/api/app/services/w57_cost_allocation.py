"""Wave 57: Cost Allocation — Cost centers, driver-based allocations, audit chain.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class CostAllocationService:
    """Domain service for Cost Allocation."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "allocation_id": "",
        "cost_center_id": "",
        "cost_center_name": "",
        "driver": "",
        "source_amount": 0.0,
        "allocated_amount": 0.0,
        "allocation_pct": 0.0,
        "period_id": "",
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_allocations(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_allocation(self, data: dict) -> dict:
        """Create a new item."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "allocation_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_allocation", "cost_allocation", item_id, {"data": data})
        return item

    def get_allocation(self, allocation_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(allocation_id)

    def recalculate(self, allocation_id: str, data: dict | None = None) -> dict | None:
        """Action: recalculate."""
        item = self._store.get(allocation_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "recalculated"
        emit_audit_event("recalculate", "cost_allocation", allocation_id, {"action": "recalculate", "data": data or {}})
        return item

    def drilldown(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def export_allocations(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = CostAllocationService()
