"""Wave 175: Evidence Graph Search v2 — Local offline index over docs, exceptions, tool traces, and audit with deterministic ordering, pagination, and saved searches.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class EvidenceSearchService:
    """Domain service for Evidence Graph Search v2."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "search_id": "",
        "query_text": "",
        "index_scope": "",
        "result_count": 0,
        "results": [],
        "order_hash": "",
        "saved": True,
        "deterministic": True,
        "status": "",
        "searched_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_searches(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def execute_search(self, data: dict) -> dict:
        """Create/run: Execute evidence search."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "search_id": item_id}
        self._store[item_id] = item
        emit_audit_event("execute_search", "evidence_search", item_id, {"data": data})
        return item

    def get_search(self, search_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(search_id)

    def save_search(self, search_id: str, data: dict | None = None) -> dict | None:
        """Action: Save search for reuse."""
        item = self._store.get(search_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "save_searchd"
        emit_audit_event("save_search", "evidence_search", search_id, {"action": "save_search", "data": data or {}})
        return item

    def open_evidence(self, search_id: str, data: dict | None = None) -> dict | None:
        """Action: Open linked evidence."""
        item = self._store.get(search_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "open_evidenced"
        emit_audit_event("open_evidence", "evidence_search", search_id, {"action": "open_evidence", "data": data or {}})
        return item

    def search_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = EvidenceSearchService()
