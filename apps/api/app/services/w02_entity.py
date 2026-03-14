"""Wave 2: Entity Management — Legal entities / business units for multi-entity close.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import uuid
import datetime as dt
from app.main import emit_audit_event


class EntityService:
    """Domain service for Entity Management."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "entity_id": "",
        "name": "",
        "code": "",
        "currency": "",
        "active": True,
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
        item = {**self._template(), **data, "entity_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create", "entity", item_id, {"data": data})
        return item

    def get(self, entity_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(entity_id)

    def update(self, entity_id: str, data: dict) -> dict | None:
        """Update an existing item."""
        item = self._store.get(entity_id)
        if not item:
            return None
        item.update(data)
        emit_audit_event("update", "entity", entity_id, {"data": data})
        return item

    def deactivate(self, entity_id: str, data: dict | None = None) -> dict | None:
        """Action: deactivate on item."""
        item = self._store.get(entity_id)
        if not item:
            return None
        if data:
            item.update(data)
        item["status"] = "deactivated" if "status" in item else item.get("status", "done")
        emit_audit_event("deactivate", "entity", entity_id, {"action": "deactivate", "data": data or {}})
        return item


# Module-level singleton
service = EntityService()
