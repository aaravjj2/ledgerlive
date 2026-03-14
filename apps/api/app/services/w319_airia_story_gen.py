"""Wave 319: Airia Story Generator v1 — Auto-write a short agent description from blueprint and capabilities (deterministic, no LLM).

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class AiriaStoryGenService:
    """Domain service for Airia Story Generator v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "story_id": "",
        "blueprint_ref": "",
        "capabilities": [],
        "generated_title": "",
        "generated_summary": "",
        "generated_highlights": [],
        "word_count": 0,
        "template_used": "",
        "content_checksum": "",
        "deterministic": True,
        "status": "",
        "generated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_stories(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def generate_story(self, data: dict) -> dict:
        """Create/run: Generate agent story."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "story_id": item_id}
        self._store[item_id] = item
        emit_audit_event("generate_story", "airia_story_gen", item_id, {"data": data})
        return item

    def get_story(self, story_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(story_id)

    def regenerate_story(self, story_id: str, data: dict | None = None) -> dict | None:
        """Action: Regenerate story."""
        item = self._store.get(story_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "regenerate_storyd"
        emit_audit_event("regenerate_story", "airia_story_gen", story_id, {"action": "regenerate_story", "data": data or {}})
        return item

    def preview_story(self, story_id: str, data: dict | None = None) -> dict | None:
        """Action: Preview story rendering."""
        item = self._store.get(story_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "preview_storyd"
        emit_audit_event("preview_story", "airia_story_gen", story_id, {"action": "preview_story", "data": data or {}})
        return item

    def story_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = AiriaStoryGenService()
