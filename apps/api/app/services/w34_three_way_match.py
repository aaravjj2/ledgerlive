"""Wave 34: Three-Way Match — PO/Receipt/Invoice matching with tolerances, variance policy, and approval for out-of-range.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ThreeWayMatchService:
    """Domain service for Three-Way Match."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "match_id": "",
        "po_id": "",
        "receipt_id": "",
        "invoice_id": "",
        "po_amount": 0.0,
        "receipt_amount": 0.0,
        "invoice_amount": 0.0,
        "variance_pct": 0.0,
        "status": "",
        "tolerance_pct": 0.0,
        "approved_by": "",
        "matched_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_matches(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_match(self, data: dict) -> dict:
        """Create a new item."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "match_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_match", "three_way_match", item_id, {"data": data})
        return item

    def get_match(self, match_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(match_id)

    def approve_variance(self, match_id: str, data: dict | None = None) -> dict | None:
        """Action: approve_variance."""
        item = self._store.get(match_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "approve_varianced"
        emit_audit_event("approve_variance", "three_way_match", match_id, {"action": "approve_variance", "data": data or {}})
        return item

    def reject_match(self, match_id: str, data: dict | None = None) -> dict | None:
        """Action: reject_match."""
        item = self._store.get(match_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "reject_matchd"
        emit_audit_event("reject_match", "three_way_match", match_id, {"action": "reject_match", "data": data or {}})
        return item

    def recalculate(self, match_id: str, data: dict | None = None) -> dict | None:
        """Action: recalculate."""
        item = self._store.get(match_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "recalculated"
        emit_audit_event("recalculate", "three_way_match", match_id, {"action": "recalculate", "data": data or {}})
        return item


# Module-level singleton
service = ThreeWayMatchService()
