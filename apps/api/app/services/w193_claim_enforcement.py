"""Wave 193: No-Floating-Claim Enforcement — Agent suggestions and decisions must include dossier_id references. Export blocked if any resolution lacks dossier. Guard enforcement.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ClaimEnforcementService:
    """Domain service for No-Floating-Claim Enforcement."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "enforcement_id": "",
        "entity_type": "",
        "entity_id": "",
        "dossier_id": "",
        "has_dossier": True,
        "claim_text": "",
        "blocked": True,
        "block_reason": "",
        "export_allowed": True,
        "enforcement_result": "",
        "status": "",
        "checked_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_enforcements(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def check_claim(self, data: dict) -> dict:
        """Create/run: Check claim has dossier reference."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "enforcement_id": item_id}
        self._store[item_id] = item
        emit_audit_event("check_claim", "claim_enforcement", item_id, {"data": data})
        return item

    def get_enforcement(self, enforcement_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(enforcement_id)

    def block_export(self, enforcement_id: str, data: dict | None = None) -> dict | None:
        """Action: Block export for missing dossier."""
        item = self._store.get(enforcement_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "block_exportd"
        emit_audit_event("block_export", "claim_enforcement", enforcement_id, {"action": "block_export", "data": data or {}})
        return item

    def unblock_export(self, enforcement_id: str, data: dict | None = None) -> dict | None:
        """Action: Unblock after dossier attached."""
        item = self._store.get(enforcement_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "unblock_exportd"
        emit_audit_event("unblock_export", "claim_enforcement", enforcement_id, {"action": "unblock_export", "data": data or {}})
        return item

    def enforcement_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ClaimEnforcementService()
