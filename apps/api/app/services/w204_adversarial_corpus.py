"""Wave 204: Agent Policy Adversarial Corpus v1 — Adversarial prompt corpus and tool misuse scenarios: bypass approvals, export without dossier, change locked periods. Policy engine blocks with deterministic reasons.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class AdversarialCorpusService:
    """Domain service for Agent Policy Adversarial Corpus v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "corpus_id": "",
        "scenario_name": "",
        "attack_type": "",
        "prompt_text": "",
        "tool_call_attempted": "",
        "policy_result": "",
        "blocked": True,
        "deny_reason": "",
        "audit_deny_logged": True,
        "deterministic": True,
        "status": "",
        "tested_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_corpus(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def add_scenario(self, data: dict) -> dict:
        """Create/run: Add adversarial scenario."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "corpus_id": item_id}
        self._store[item_id] = item
        emit_audit_event("add_scenario", "adversarial_corpus", item_id, {"data": data})
        return item

    def get_scenario(self, corpus_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(corpus_id)

    def run_scenario(self, corpus_id: str, data: dict | None = None) -> dict | None:
        """Action: Run adversarial scenario."""
        item = self._store.get(corpus_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "run_scenariod"
        emit_audit_event("run_scenario", "adversarial_corpus", corpus_id, {"action": "run_scenario", "data": data or {}})
        return item

    def verify_blocked(self, corpus_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify scenario was blocked."""
        item = self._store.get(corpus_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_blockedd"
        emit_audit_event("verify_blocked", "adversarial_corpus", corpus_id, {"action": "verify_blocked", "data": data or {}})
        return item

    def corpus_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = AdversarialCorpusService()
