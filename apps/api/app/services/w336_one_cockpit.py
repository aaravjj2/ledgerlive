"""Wave 336: One Cockpit v1 — Race Control as default home route with minimal cognitive load polish.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class OneCockpitService:
    """Domain service for One Cockpit v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "cockpit_id": "",
        "layout_config": {},
        "visible_sections": [],
        "hidden_sections": [],
        "default_route": "",
        "cognitive_load_score": 0.0,
        "section_order": [],
        "user_prefs": {},
        "is_home": True,
        "deterministic": True,
        "status": "",
        "configured_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_cockpits(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_cockpit(self, data: dict) -> dict:
        """Create/run: Create cockpit config."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "cockpit_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_cockpit", "one_cockpit", item_id, {"data": data})
        return item

    def get_cockpit(self, cockpit_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(cockpit_id)

    def set_default(self, cockpit_id: str, data: dict | None = None) -> dict | None:
        """Action: Set as default home."""
        item = self._store.get(cockpit_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "set_defaultd"
        emit_audit_event("set_default", "one_cockpit", cockpit_id, {"action": "set_default", "data": data or {}})
        return item

    def customize_layout(self, cockpit_id: str, data: dict | None = None) -> dict | None:
        """Action: Customize layout."""
        item = self._store.get(cockpit_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "customize_layoutd"
        emit_audit_event("customize_layout", "one_cockpit", cockpit_id, {"action": "customize_layout", "data": data or {}})
        return item

    def cockpit_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = OneCockpitService()
