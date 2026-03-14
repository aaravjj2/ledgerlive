"""Wave 251: Policy Events v1 — Policy denies, scope violations, and injection flags become structured security events with classification, evidence, and deterministic reasons.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class PolicyEventsService:
    """Domain service for Policy Events v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "event_id": "",
        "event_type": "",
        "policy_ref": "",
        "violation_type": "",
        "severity": "",
        "classification": "",
        "evidence": {},
        "deny_reason": "",
        "source_context": {},
        "affected_entities": [],
        "remediation_hint": "",
        "status": "",
        "detected_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_events(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_event(self, data: dict) -> dict:
        """Create/run: Create policy event."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "event_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_event", "policy_events", item_id, {"data": data})
        return item

    def get_event(self, event_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(event_id)

    def classify_event(self, event_id: str, data: dict | None = None) -> dict | None:
        """Action: Classify policy event."""
        item = self._store.get(event_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "classify_eventd"
        emit_audit_event("classify_event", "policy_events", event_id, {"action": "classify_event", "data": data or {}})
        return item

    def link_evidence(self, event_id: str, data: dict | None = None) -> dict | None:
        """Action: Link evidence to event."""
        item = self._store.get(event_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "link_evidenced"
        emit_audit_event("link_evidence", "policy_events", event_id, {"action": "link_evidence", "data": data or {}})
        return item

    def event_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = PolicyEventsService()
