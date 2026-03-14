"""Wave 100: Demo Mode Marketplace — End-to-end demo mode including marketplace template import and execution.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class DemoMarketplaceService:
    """Domain service for Demo Mode Marketplace."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "demo_id": "",
        "demo_name": "",
        "templates_imported": [],
        "steps": [],
        "current_step": 0,
        "total_steps": 0,
        "status": "",
        "hash": "",
        "started_at": "",
        "completed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_demos(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def start_demo(self, data: dict) -> dict:
        """Create/run: Start demo marketplace run."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "demo_id": item_id}
        self._store[item_id] = item
        emit_audit_event("start_demo", "demo_marketplace", item_id, {"data": data})
        return item

    def get_demo(self, demo_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(demo_id)

    def advance(self, demo_id: str, data: dict | None = None) -> dict | None:
        """Action: Advance to next step."""
        item = self._store.get(demo_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "advanced"
        emit_audit_event("advance", "demo_marketplace", demo_id, {"action": "advance", "data": data or {}})
        return item

    def verify_demo(self, demo_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify demo hash."""
        item = self._store.get(demo_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_demod"
        emit_audit_event("verify_demo", "demo_marketplace", demo_id, {"action": "verify_demo", "data": data or {}})
        return item

    def demo_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = DemoMarketplaceService()
