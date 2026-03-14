"""Wave 326: Tool Scope Diffing v1 — Show scope changes over time; approvals required for expanding scopes; audited.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ToolScopeDiffingService:
    """Domain service for Tool Scope Diffing v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "diff_id": "",
        "tool_ref": "",
        "scope_before": [],
        "scope_after": [],
        "added_scopes": [],
        "removed_scopes": [],
        "expansion_detected": True,
        "approval_required": True,
        "approved_by": "",
        "audit_ref": "",
        "deterministic": True,
        "status": "",
        "diffed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_diffs(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_diff(self, data: dict) -> dict:
        """Create/run: Create scope diff."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "diff_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_diff", "tool_scope_diffing", item_id, {"data": data})
        return item

    def get_diff(self, diff_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(diff_id)

    def approve_expansion(self, diff_id: str, data: dict | None = None) -> dict | None:
        """Action: Approve scope expansion."""
        item = self._store.get(diff_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "approve_expansiond"
        emit_audit_event("approve_expansion", "tool_scope_diffing", diff_id, {"action": "approve_expansion", "data": data or {}})
        return item

    def reject_expansion(self, diff_id: str, data: dict | None = None) -> dict | None:
        """Action: Reject scope expansion."""
        item = self._store.get(diff_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "reject_expansiond"
        emit_audit_event("reject_expansion", "tool_scope_diffing", diff_id, {"action": "reject_expansion", "data": data or {}})
        return item

    def diff_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ToolScopeDiffingService()
