"""Wave 261: Replay Viewer v3 — Diffing between original and replay artifacts. Jump-to-evidence and jump-to-policy-event navigation with deterministic rendering.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ReplayViewerV3Service:
    """Domain service for Replay Viewer v3."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "viewer_id": "",
        "original_ref": "",
        "replay_ref": "",
        "diff_entries": [],
        "diff_summary": {},
        "evidence_links": [],
        "policy_event_links": [],
        "match_pct": 0.0,
        "divergence_points": [],
        "render_hash": "",
        "navigation_index": {},
        "status": "",
        "compared_at": "",
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
        """Create/run: Create replay viewer comparison."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "viewer_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_viewer", "replay_viewer_v3", item_id, {"data": data})
        return item

    def get_viewer(self, viewer_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(viewer_id)

    def compute_diff(self, viewer_id: str, data: dict | None = None) -> dict | None:
        """Action: Compute artifact diff."""
        item = self._store.get(viewer_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "compute_diffd"
        emit_audit_event("compute_diff", "replay_viewer_v3", viewer_id, {"action": "compute_diff", "data": data or {}})
        return item

    def jump_to_evidence(self, viewer_id: str, data: dict | None = None) -> dict | None:
        """Action: Jump to evidence."""
        item = self._store.get(viewer_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "jump_to_evidenced"
        emit_audit_event("jump_to_evidence", "replay_viewer_v3", viewer_id, {"action": "jump_to_evidence", "data": data or {}})
        return item

    def viewer_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ReplayViewerV3Service()
