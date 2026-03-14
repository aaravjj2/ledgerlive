"""Wave 250 — Health Dashboard v1: system health aggregation with component status."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class HealthEntry:
    entry_id: str
    component: str
    details: dict
    status: str = "active"
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


class HealthDashboardService:
    def __init__(self):
        self._items: dict[str, HealthEntry] = {}
        self._audit: list[dict[str, Any]] = []

    def _log(self, action: str, data: dict | None = None):
        self._audit.append({"ts": datetime.now(timezone.utc).isoformat(), "action": action, **(data or {})})

    def create(self, component: str, status: str, details: dict) -> HealthEntry:
        item_id = uuid.uuid4().hex[:12]
        item = HealthEntry(
            entry_id=item_id,
            component=component,
            status=status,
            details=details,
        )
        self._items[item_id] = item
        self._log("created", {"entry_id": item_id})
        return item

    def get(self, item_id: str) -> HealthEntry:
        if item_id not in self._items:
            raise KeyError(f"HealthEntry not found: {item_id}")
        return self._items[item_id]

    def list_all(self) -> list[HealthEntry]:
        return list(self._items.values())

    def update_status(self, item_id: str, status: str) -> HealthEntry:
        item = self.get(item_id)
        item.status = status
        self._log("status_updated", {"entry_id": item_id, "status": status})
        return item

    def delete(self, item_id: str) -> dict:
        item = self.get(item_id)
        del self._items[item_id]
        self._log("deleted", {"entry_id": item_id})
        return {"deleted": item_id}

    def get_audit(self) -> list[dict[str, Any]]:
        return list(self._audit)


_svc: HealthDashboardService | None = None


def get_health_dashboard_service() -> HealthDashboardService:
    global _svc
    if _svc is None:
        _svc = HealthDashboardService()
    return _svc


def reset_health_dashboard_service():
    global _svc
    _svc = None
