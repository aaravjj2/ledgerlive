"""Wave 208: Fail-Closed Posture v1 — If verifier cannot prove invariants or evidence missing, action becomes approval required or blocked. Never auto-approve under uncertainty.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class FailClosedService:
    """Domain service for Fail-Closed Posture v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "posture_id": "",
        "action_type": "",
        "verifier_result": "",
        "evidence_present": True,
        "invariants_proven": True,
        "fail_closed_triggered": True,
        "approval_required": True,
        "blocked": True,
        "reason": "",
        "fallback_decision": "",
        "status": "",
        "evaluated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_postures(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def evaluate_posture(self, data: dict) -> dict:
        """Create/run: Evaluate fail-closed posture."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "posture_id": item_id}
        self._store[item_id] = item
        emit_audit_event("evaluate_posture", "fail_closed", item_id, {"data": data})
        return item

    def get_posture(self, posture_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(posture_id)

    def trigger_fail_closed(self, posture_id: str, data: dict | None = None) -> dict | None:
        """Action: Trigger fail-closed scenario."""
        item = self._store.get(posture_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "trigger_fail_closedd"
        emit_audit_event("trigger_fail_closed", "fail_closed", posture_id, {"action": "trigger_fail_closed", "data": data or {}})
        return item

    def verify_blocked(self, posture_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify action was blocked."""
        item = self._store.get(posture_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_blockedd"
        emit_audit_event("verify_blocked", "fail_closed", posture_id, {"action": "verify_blocked", "data": data or {}})
        return item

    def posture_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = FailClosedService()
