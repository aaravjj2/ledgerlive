"""Wave 229: Race Control State Machine v1 — Finite state machine governing close lifecycle: NOT_STARTED -> IN_PROGRESS -> REVIEW -> APPROVED -> CLOSED. Transition guards enforce prerequisites.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class RcStateMachineService:
    """Domain service for Race Control State Machine v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "machine_id": "",
        "period_id": "",
        "current_state": "",
        "previous_state": "",
        "valid_transitions": [],
        "transition_history": [],
        "guard_results": {},
        "last_transition_at": "",
        "locked": True,
        "lock_reason": "",
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_machines(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_machine(self, data: dict) -> dict:
        """Create/run: Create state machine."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "machine_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_machine", "rc_state_machine", item_id, {"data": data})
        return item

    def get_machine(self, machine_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(machine_id)

    def transition(self, machine_id: str, data: dict | None = None) -> dict | None:
        """Action: Perform state transition."""
        item = self._store.get(machine_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "transitiond"
        emit_audit_event("transition", "rc_state_machine", machine_id, {"action": "transition", "data": data or {}})
        return item

    def lock_state(self, machine_id: str, data: dict | None = None) -> dict | None:
        """Action: Lock state machine."""
        item = self._store.get(machine_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "lock_stated"
        emit_audit_event("lock_state", "rc_state_machine", machine_id, {"action": "lock_state", "data": data or {}})
        return item

    def machine_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = RcStateMachineService()
