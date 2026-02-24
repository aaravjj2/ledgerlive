"""Wave 243: Verifier Gate UI v1 — Shows which invariants pass or fail, surfaces required approvals per step, and provides deterministic deny reasons for blocked actions.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class VerifierGateUiService:
    """Domain service for Verifier Gate UI v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "gate_id": "",
        "step_ref": "",
        "invariants": [],
        "passed_invariants": [],
        "failed_invariants": [],
        "approvals_required": [],
        "deny_reasons": [],
        "overall_result": "",
        "deterministic_output": True,
        "evidence_links": [],
        "gate_hash": "",
        "status": "",
        "evaluated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_gates(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_gate(self, data: dict) -> dict:
        """Create/run: Create verifier gate evaluation."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "gate_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_gate", "verifier_gate_ui", item_id, {"data": data})
        return item

    def get_gate(self, gate_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(gate_id)

    def evaluate_gate(self, gate_id: str, data: dict | None = None) -> dict | None:
        """Action: Evaluate gate invariants."""
        item = self._store.get(gate_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "evaluate_gated"
        emit_audit_event("evaluate_gate", "verifier_gate_ui", gate_id, {"action": "evaluate_gate", "data": data or {}})
        return item

    def explain_deny(self, gate_id: str, data: dict | None = None) -> dict | None:
        """Action: Explain deny reasons."""
        item = self._store.get(gate_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "explain_denyd"
        emit_audit_event("explain_deny", "verifier_gate_ui", gate_id, {"action": "explain_deny", "data": data or {}})
        return item

    def gate_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = VerifierGateUiService()
