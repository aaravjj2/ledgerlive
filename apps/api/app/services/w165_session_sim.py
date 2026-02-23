"""Wave 165: Live Session Simulator — Deterministic agent session replay runner: streams transcript events, triggers tool calls, streams verifier outcomes and tool trace updates.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class SessionSimService:
    """Domain service for Live Session Simulator."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "session_id": "",
        "session_name": "",
        "transcript": [],
        "tool_calls": [],
        "verifier_outcomes": [],
        "transcript_hash": "",
        "tool_trace_hash": "",
        "duration_ms": 0.0,
        "status": "",
        "started_at": "",
        "completed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_sessions(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def start_session(self, data: dict) -> dict:
        """Create/run: Start a simulator session."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "session_id": item_id}
        self._store[item_id] = item
        emit_audit_event("start_session", "session_sim", item_id, {"data": data})
        return item

    def get_session(self, session_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(session_id)

    def advance_session(self, session_id: str, data: dict | None = None) -> dict | None:
        """Action: Advance session step."""
        item = self._store.get(session_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "advance_sessiond"
        emit_audit_event("advance_session", "session_sim", session_id, {"action": "advance_session", "data": data or {}})
        return item

    def complete_session(self, session_id: str, data: dict | None = None) -> dict | None:
        """Action: Complete session."""
        item = self._store.get(session_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "complete_sessiond"
        emit_audit_event("complete_session", "session_sim", session_id, {"action": "complete_session", "data": data or {}})
        return item

    def session_transcript(self, session_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(session_id)

    def session_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = SessionSimService()
