"""Wave 166: Agent Console UI — Ops-grade agent console: transcript stream, tool trace stream, verifier results, approvals inbox, run status, export links.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class AgentConsoleService:
    """Domain service for Agent Console UI."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "console_id": "",
        "session_id": "",
        "transcript_items": [],
        "tool_trace_items": [],
        "verifier_items": [],
        "approvals_pending": [],
        "run_status": "",
        "export_links": [],
        "page_testid": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_consoles(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_console(self, data: dict) -> dict:
        """Create/run: Create agent console session."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "console_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_console", "agent_console", item_id, {"data": data})
        return item

    def get_console(self, console_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(console_id)

    def refresh_console(self, console_id: str, data: dict | None = None) -> dict | None:
        """Action: Refresh console data."""
        item = self._store.get(console_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "refresh_consoled"
        emit_audit_event("refresh_console", "agent_console", console_id, {"action": "refresh_console", "data": data or {}})
        return item

    def approve_item(self, console_id: str, data: dict | None = None) -> dict | None:
        """Action: Approve item from console."""
        item = self._store.get(console_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "approve_itemd"
        emit_audit_event("approve_item", "agent_console", console_id, {"action": "approve_item", "data": data or {}})
        return item

    def export_from_console(self, console_id: str, data: dict | None = None) -> dict | None:
        """Action: Export from console."""
        item = self._store.get(console_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "export_from_consoled"
        emit_audit_event("export_from_console", "agent_console", console_id, {"action": "export_from_console", "data": data or {}})
        return item

    def console_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = AgentConsoleService()
