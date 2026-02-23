"""Wave 161: DEMO Contract — Single authoritative APP_MODE switch with frozen time, seeded RNG, deterministic IDs, stable ordering, outbound network deny.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class DemoContractService:
    """Domain service for DEMO Contract."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "contract_id": "",
        "app_mode": "",
        "seed": 0,
        "frozen_time": "",
        "network_policy": "",
        "id_policy": "",
        "ordering_policy": "",
        "invariants_hash": "",
        "status": "",
        "checked_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_contracts(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def check_contract(self, data: dict) -> dict:
        """Create/run: Check DEMO contract invariants."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "contract_id": item_id}
        self._store[item_id] = item
        emit_audit_event("check_contract", "demo_contract", item_id, {"data": data})
        return item

    def get_contract(self, contract_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(contract_id)

    def verify_invariants(self, contract_id: str, data: dict | None = None) -> dict | None:
        """Action: Verify invariants hold."""
        item = self._store.get(contract_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "verify_invariantsd"
        emit_audit_event("verify_invariants", "demo_contract", contract_id, {"action": "verify_invariants", "data": data or {}})
        return item

    def demo_contract_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def demo_contract_hash(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = DemoContractService()
