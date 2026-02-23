"""Wave 211: Replay Viewer UI v1 — UI page Replay: timeline of steps, tool trace rows linked to dossiers, evidence span viewer. Fully data-testid instrumented.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ReplayViewerService:
    """Domain service for Replay Viewer UI v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "viewer_id": "",
        "replay_id": "",
        "timeline_steps": [],
        "tool_trace_rows": [],
        "dossier_links": [],
        "evidence_spans": [],
        "current_step_index": 0,
        "page_testid": "",
        "highlight_active": True,
        "status": "",
        "opened_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_viewers(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_viewer(self, data: dict) -> dict:
        """Create/run: Create replay viewer session."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "viewer_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_viewer", "replay_viewer", item_id, {"data": data})
        return item

    def get_viewer(self, viewer_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(viewer_id)

    def step_forward(self, viewer_id: str, data: dict | None = None) -> dict | None:
        """Action: Step forward in timeline."""
        item = self._store.get(viewer_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "step_forwardd"
        emit_audit_event("step_forward", "replay_viewer", viewer_id, {"action": "step_forward", "data": data or {}})
        return item

    def open_dossier(self, viewer_id: str, data: dict | None = None) -> dict | None:
        """Action: Open linked dossier."""
        item = self._store.get(viewer_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "open_dossierd"
        emit_audit_event("open_dossier", "replay_viewer", viewer_id, {"action": "open_dossier", "data": data or {}})
        return item

    def highlight_evidence(self, viewer_id: str, data: dict | None = None) -> dict | None:
        """Action: Highlight evidence span."""
        item = self._store.get(viewer_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "highlight_evidenced"
        emit_audit_event("highlight_evidence", "replay_viewer", viewer_id, {"action": "highlight_evidence", "data": data or {}})
        return item

    def viewer_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ReplayViewerService()
