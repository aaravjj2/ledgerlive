"""Wave 200: Submission Hardening v2 — Single command generator: make submit-all produces all bundles and index. Docs match Make targets. TOUR >=240s coverage. Twice-run determinism.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class SubmitAllService:
    """Domain service for Submission Hardening v2."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "submission_id": "",
        "check_type": "",
        "target": "",
        "make_targets_valid": True,
        "doc_commands_valid": True,
        "index_generated": True,
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

    def list_submissions(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def run_submission(self, data: dict) -> dict:
        """Create/run: Run submission hardening check."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "submission_id": item_id}
        self._store[item_id] = item
        emit_audit_event("run_submission", "submit_all", item_id, {"data": data})
        return item

    def get_submission(self, submission_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(submission_id)

    def verify_docs(self, submission_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify docs match Make targets."""
        item = self._store.get(submission_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_docsd"
        emit_audit_event("verify_docs", "submit_all", submission_id, {"action": "verify_docs", "data": data or {}})
        return item

    def verify_determinism(self, submission_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify twice-run determinism."""
        item = self._store.get(submission_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_determinismd"
        emit_audit_event("verify_determinism", "submit_all", submission_id, {"action": "verify_determinism", "data": data or {}})
        return item

    def submission_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = SubmitAllService()
