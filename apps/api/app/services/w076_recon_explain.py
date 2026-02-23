"""Wave 76: Reconciliation Explainability — Reason DAG for reconciliation decisions with evidence pointers.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ReconExplainService:
    """Domain service for Reconciliation Explainability."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "explain_id": "",
        "recon_id": "",
        "reason_dag": {},
        "evidence_pointers": [],
        "confidence": 0.0,
        "explanation_text": "",
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_explanations(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def generate_explanation(self, data: dict) -> dict:
        """Create/run: Generate reconciliation explanation."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "explain_id": item_id}
        self._store[item_id] = item
        emit_audit_event("generate_explanation", "recon_explain", item_id, {"data": data})
        return item

    def get_explanation(self, explain_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(explain_id)

    def add_evidence(self, explain_id: str, data: dict | None = None) -> dict | None:
        """Action: Add evidence pointer."""
        item = self._store.get(explain_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "add_evidenced"
        emit_audit_event("add_evidence", "recon_explain", explain_id, {"action": "add_evidence", "data": data or {}})
        return item

    def verify_dag(self, explain_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify reason DAG."""
        item = self._store.get(explain_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_dagd"
        emit_audit_event("verify_dag", "recon_explain", explain_id, {"action": "verify_dag", "data": data or {}})
        return item

    def export_explanations(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ReconExplainService()
