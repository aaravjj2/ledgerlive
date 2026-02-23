"""Wave 169: Connector Mock Servers v1 — Local mock servers for QBO/Xero/Plaid simulating pagination, token refresh, 429 backoff, partial responses, dirty data.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class ConnectorMocksService:
    """Domain service for Connector Mock Servers v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "mock_id": "",
        "provider": "",
        "mock_type": "",
        "endpoint": "",
        "response_mode": "",
        "pagination_enabled": True,
        "token_refresh_sim": True,
        "error_rate_pct": 0.0,
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_mocks(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_mock(self, data: dict) -> dict:
        """Create/run: Create mock server config."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "mock_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_mock", "connector_mocks", item_id, {"data": data})
        return item

    def get_mock(self, mock_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(mock_id)

    def toggle_error(self, mock_id: str, data: dict | None = None) -> dict | None:
        """Action: Toggle error simulation."""
        item = self._store.get(mock_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "toggle_errord"
        emit_audit_event("toggle_error", "connector_mocks", mock_id, {"action": "toggle_error", "data": data or {}})
        return item

    def sync_mock(self, mock_id: str, data: dict | None = None) -> dict | None:
        """Action: Sync data from mock."""
        item = self._store.get(mock_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "sync_mockd"
        emit_audit_event("sync_mock", "connector_mocks", mock_id, {"action": "sync_mock", "data": data or {}})
        return item

    def mock_status(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def mock_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = ConnectorMocksService()
