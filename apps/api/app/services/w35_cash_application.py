"""Wave 35: Cash Application — AR allocations, partial payments, deduction/dispute workflow.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class CashApplicationService:
    """Domain service for Cash Application."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "application_id": "",
        "customer_id": "",
        "invoice_id": "",
        "payment_amount": 0.0,
        "applied_amount": 0.0,
        "remaining": 0.0,
        "status": "",
        "dispute_reason": "",
        "resolved_at": "",
        "applied_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def apply(self, data: dict) -> dict:
        """Create a new item."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "application_id": item_id}
        self._store[item_id] = item
        emit_audit_event("apply", "cash_application", item_id, {"data": data})
        return item

    def get(self, application_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(application_id)

    def dispute(self, application_id: str, data: dict | None = None) -> dict | None:
        """Action: dispute."""
        item = self._store.get(application_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "disputed"
        emit_audit_event("dispute", "cash_application", application_id, {"action": "dispute", "data": data or {}})
        return item

    def resolve_dispute(self, application_id: str, data: dict | None = None) -> dict | None:
        """Action: resolve_dispute."""
        item = self._store.get(application_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "resolve_disputed"
        emit_audit_event("resolve_dispute", "cash_application", application_id, {"action": "resolve_dispute", "data": data or {}})
        return item

    def export_ar(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = CashApplicationService()
