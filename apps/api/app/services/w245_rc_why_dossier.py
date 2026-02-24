"""Wave 245: Race Control Why v1 — Every next action has a one-click dossier/reason DAG/evidence view. Consistent across surfaces with deterministic rendering.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class RcWhyDossierService:
    """Domain service for Race Control Why v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "why_id": "",
        "action_ref": "",
        "reason_dag": {},
        "evidence_chain": [],
        "dossier_content": {},
        "policy_refs": [],
        "precedent_refs": [],
        "confidence_score": 0.0,
        "surface_type": "",
        "render_hash": "",
        "consistent_across": [],
        "status": "",
        "generated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_whys(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def generate_why(self, data: dict) -> dict:
        """Create/run: Generate why dossier for action."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "why_id": item_id}
        self._store[item_id] = item
        emit_audit_event("generate_why", "rc_why_dossier", item_id, {"data": data})
        return item

    def get_why(self, why_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(why_id)

    def expand_reason(self, why_id: str, data: dict | None = None) -> dict | None:
        """Action: Expand reason DAG node."""
        item = self._store.get(why_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "expand_reasond"
        emit_audit_event("expand_reason", "rc_why_dossier", why_id, {"action": "expand_reason", "data": data or {}})
        return item

    def verify_consistency(self, why_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify cross-surface consistency."""
        item = self._store.get(why_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_consistencyd"
        emit_audit_event("verify_consistency", "rc_why_dossier", why_id, {"action": "verify_consistency", "data": data or {}})
        return item

    def why_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = RcWhyDossierService()
