"""Wave 50: Judge Demo 2.0 — Scripted 4-min demo script: seed, ingest, reconcile, override, export, verify.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class JudgeDemoV2Service:
    """Domain service for Judge Demo 2.0."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "demo_id": "",
        "demo_name": "",
        "steps": [],
        "current_step": 0,
        "total_steps": 0,
        "status": "",
        "duration_seconds": 0.0,
        "hash": "",
        "started_at": "",
        "completed_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_demos(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def start_demo(self, data: dict) -> dict:
        """Create a new item."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "demo_id": item_id}
        self._store[item_id] = item
        emit_audit_event("start_demo", "judge_demo_v2", item_id, {"data": data})
        return item

    def get_demo(self, demo_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(demo_id)

    def advance_step(self, demo_id: str, data: dict | None = None) -> dict | None:
        """Action: advance_step."""
        item = self._store.get(demo_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "advance_stepd"
        emit_audit_event("advance_step", "judge_demo_v2", demo_id, {"action": "advance_step", "data": data or {}})
        return item

    def verify_demo(self, demo_id: str, data: dict | None = None) -> dict | None:
        """Action: verify_demo."""
        item = self._store.get(demo_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_demod"
        emit_audit_event("verify_demo", "judge_demo_v2", demo_id, {"action": "verify_demo", "data": data or {}})
        return item

    def reset_demo(self, demo_id: str, data: dict | None = None) -> dict | None:
        """Action: reset_demo."""
        item = self._store.get(demo_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "reset_demod"
        emit_audit_event("reset_demo", "judge_demo_v2", demo_id, {"action": "reset_demo", "data": data or {}})
        return item

    def script_template(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = JudgeDemoV2Service()
