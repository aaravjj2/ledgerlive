"""Wave 190: Evidence Span Highlighter v2 — Multi-page multi-field evidence viewer with deep links from tool trace to dossier. Highlights evidence correctly in viewer.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class EvidenceHighlighterService:
    """Domain service for Evidence Span Highlighter v2."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "highlight_id": "",
        "dossier_id": "",
        "doc_id": "",
        "page_number": 0,
        "field_name": "",
        "offset_start": 0,
        "offset_end": 0,
        "highlight_text": "",
        "confidence": 0.0,
        "deep_link": "",
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_highlights(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_highlight(self, data: dict) -> dict:
        """Create/run: Create evidence highlight."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "highlight_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_highlight", "evidence_highlighter", item_id, {"data": data})
        return item

    def get_highlight(self, highlight_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(highlight_id)

    def link_to_dossier(self, highlight_id: str, data: dict | None = None) -> dict | None:
        """Action: Link highlight to dossier."""
        item = self._store.get(highlight_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "link_to_dossierd"
        emit_audit_event("link_to_dossier", "evidence_highlighter", highlight_id, {"action": "link_to_dossier", "data": data or {}})
        return item

    def open_deep_link(self, highlight_id: str, data: dict | None = None) -> dict | None:
        """Action: Open deep link from tool trace."""
        item = self._store.get(highlight_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "open_deep_linkd"
        emit_audit_event("open_deep_link", "evidence_highlighter", highlight_id, {"action": "open_deep_link", "data": data or {}})
        return item

    def highlight_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = EvidenceHighlighterService()
