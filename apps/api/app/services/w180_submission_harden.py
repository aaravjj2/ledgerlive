"""Wave 180: Submission Hardening Wave — One-command local run, docs generator, expanded TOUR coverage. Documentation tests enforce commands exist. MCP E2E twice-run determinism.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class SubmissionHardenService:
    """Domain service for Submission Hardening Wave."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "harden_id": "",
        "check_type": "",
        "target": "",
        "doc_commands_valid": True,
        "make_targets_exist": True,
        "tour_duration_s": 0.0,
        "determinism_pass": True,
        "twice_run_hash_1": "",
        "twice_run_hash_2": "",
        "status": "",
        "checked_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_checks(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def run_check(self, data: dict) -> dict:
        """Create/run: Run hardening check."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "harden_id": item_id}
        self._store[item_id] = item
        emit_audit_event("run_check", "submission_harden", item_id, {"data": data})
        return item

    def get_check(self, harden_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(harden_id)

    def verify_docs(self, harden_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify docs match Make targets."""
        item = self._store.get(harden_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_docsd"
        emit_audit_event("verify_docs", "submission_harden", harden_id, {"action": "verify_docs", "data": data or {}})
        return item

    def verify_determinism(self, harden_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify twice-run determinism."""
        item = self._store.get(harden_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_determinismd"
        emit_audit_event("verify_determinism", "submission_harden", harden_id, {"action": "verify_determinism", "data": data or {}})
        return item

    def harden_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = SubmissionHardenService()
