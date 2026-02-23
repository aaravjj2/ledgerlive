"""Wave 7: Exception Management — Taxonomy-based exception triage for reconciliation mismatches.

PROJECT_ID: LEDGERLIVE
"""
import uuid
import datetime as dt
from app.main import emit_audit_event


class ExceptionService:
    """Domain service for Exception Management."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "exception_id": "",
        "recon_id": "",
        "category": "",
        "severity": "",
        "description": "",
        "status": "",
        "assigned_to": "",
        "resolved_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list(self, **kwargs) -> list[dict]:
        """List items with optional filters."""
        items = list(self._store.values())
        limit = kwargs.get("limit", 100)
        return items[:limit]

    def create(self, data: dict) -> dict:
        """Create a new item."""
        item_id = str(uuid.uuid4())
        item = {**self._template(), **data, "exception_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create", "exception", item_id, {"data": data})
        return item

    def get(self, exception_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(exception_id)

    def assign(self, exception_id: str, data: dict | None = None) -> dict | None:
        """Action: assign on item."""
        item = self._store.get(exception_id)
        if not item:
            return None
        if data:
            item.update(data)
        item["status"] = "assignd" if "status" in item else item.get("status", "done")
        emit_audit_event("assign", "exception", exception_id, {"action": "assign", "data": data or {}})
        return item

    def resolve(self, exception_id: str, data: dict | None = None) -> dict | None:
        """Action: resolve on item."""
        item = self._store.get(exception_id)
        if not item:
            return None
        if data:
            item.update(data)
        item["status"] = "resolved" if "status" in item else item.get("status", "done")
        emit_audit_event("resolve", "exception", exception_id, {"action": "resolve", "data": data or {}})
        return item


# Module-level singleton
service = ExceptionService()
