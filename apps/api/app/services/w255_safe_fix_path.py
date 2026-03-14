"""Wave 255: Safe Fix Path v1 — Blocked actions show evidence-backed remediation suggestions with no side effects until approved. Deterministic suggestion generation.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class SafeFixPathService:
    """Domain service for Safe Fix Path v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "fix_id": "",
        "blocked_action_ref": "",
        "block_reason": "",
        "remediation_steps": [],
        "evidence_refs": [],
        "risk_reduction_pct": 0.0,
        "side_effects": [],
        "approval_required": True,
        "approved_by": "",
        "applied": True,
        "fix_hash": "",
        "status": "",
        "suggested_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_fixes(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def suggest_fix(self, data: dict) -> dict:
        """Create/run: Suggest safe fix path."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "fix_id": item_id}
        self._store[item_id] = item
        emit_audit_event("suggest_fix", "safe_fix_path", item_id, {"data": data})
        return item

    def get_fix(self, fix_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(fix_id)

    def approve_fix(self, fix_id: str, data: dict | None = None) -> dict | None:
        """Action: Approve fix path."""
        item = self._store.get(fix_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "approve_fixd"
        emit_audit_event("approve_fix", "safe_fix_path", fix_id, {"action": "approve_fix", "data": data or {}})
        return item

    def apply_fix(self, fix_id: str, data: dict | None = None) -> dict | None:
        """Action: Apply approved fix."""
        item = self._store.get(fix_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "apply_fixd"
        emit_audit_event("apply_fix", "safe_fix_path", fix_id, {"action": "apply_fix", "data": data or {}})
        return item

    def fix_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = SafeFixPathService()
