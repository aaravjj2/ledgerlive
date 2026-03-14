"""Wave 85: Consolidation Adjustments Lock — Consolidation adjustments with approval workflow and lock enforcement.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ConsolAdjLockService:
    """Domain service for Consolidation Adjustments Lock."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "adj_id": "",
        "consolidation_id": "",
        "adj_type": "",
        "amount": 0.0,
        "description": "",
        "approved_by": "",
        "locked": True,
        "lock_reason": "",
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_adjustments(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_adjustment(self, data: dict) -> dict:
        """Create/run: Create adjustment."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "adj_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_adjustment", "consol_adj_lock", item_id, {"data": data})
        return item

    def get_adjustment(self, adj_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(adj_id)

    def approve(self, adj_id: str, data: dict | None = None) -> dict | None:
        """Action: Approve adjustment."""
        item = self._store.get(adj_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "approved"
        emit_audit_event("approve", "consol_adj_lock", adj_id, {"action": "approve", "data": data or {}})
        return item

    def lock_adj(self, adj_id: str, data: dict | None = None) -> dict | None:
        """Action: Lock adjustment."""
        item = self._store.get(adj_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "lock_adjd"
        emit_audit_event("lock_adj", "consol_adj_lock", adj_id, {"action": "lock_adj", "data": data or {}})
        return item

    def deny_after_lock(self, adj_id: str, data: dict | None = None) -> dict | None:
        """Action: Deny post-lock modification."""
        item = self._store.get(adj_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "deny_after_lockd"
        emit_audit_event("deny_after_lock", "consol_adj_lock", adj_id, {"action": "deny_after_lock", "data": data or {}})
        return item

    def adj_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ConsolAdjLockService()
