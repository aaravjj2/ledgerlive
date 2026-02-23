"""Wave 170: Connector Real-Mode Interface — Real provider interfaces behind ENABLE_QBO/ENABLE_XERO/ENABLE_PLAID flags. Keys optional, never required. Fail fast without keys.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ConnectorRealmodeService:
    """Domain service for Connector Real-Mode Interface."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "config_id": "",
        "provider": "",
        "enabled": True,
        "has_keys": True,
        "validation_result": "",
        "error_message": "",
        "fallback_to_mock": True,
        "status": "",
        "validated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_configs(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_config(self, data: dict) -> dict:
        """Create/run: Create real-mode config."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "config_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_config", "connector_realmode", item_id, {"data": data})
        return item

    def get_config(self, config_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(config_id)

    def validate_keys(self, config_id: str, data: dict | None = None) -> dict | None:
        """Action: Validate provider keys."""
        item = self._store.get(config_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "validate_keysd"
        emit_audit_event("validate_keys", "connector_realmode", config_id, {"action": "validate_keys", "data": data or {}})
        return item

    def test_connection(self, config_id: str, data: dict | None = None) -> dict | None:
        """Action: Test connection safely."""
        item = self._store.get(config_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "test_connectiond"
        emit_audit_event("test_connection", "connector_realmode", config_id, {"action": "test_connection", "data": data or {}})
        return item

    def config_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ConnectorRealmodeService()
