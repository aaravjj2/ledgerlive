"""Wave 257: Tamper Simulation v1 — DEMO-only mode that injects controlled integrity failures. UI explains detection and recovery process with deterministic outcomes.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class TamperSimulationService:
    """Domain service for Tamper Simulation v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "simulation_id": "",
        "target_entity": "",
        "tamper_type": "",
        "injected_failure": {},
        "detection_method": "",
        "detected": True,
        "detection_latency_ms": 0,
        "recovery_steps": [],
        "recovery_successful": True,
        "explanation": "",
        "simulation_hash": "",
        "status": "",
        "simulated_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_simulations(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def run_simulation(self, data: dict) -> dict:
        """Create/run: Run tamper simulation."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "simulation_id": item_id}
        self._store[item_id] = item
        emit_audit_event("run_simulation", "tamper_simulation", item_id, {"data": data})
        return item

    def get_simulation(self, simulation_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(simulation_id)

    def inject_failure(self, simulation_id: str, data: dict | None = None) -> dict | None:
        """Action: Inject controlled failure."""
        item = self._store.get(simulation_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "inject_failured"
        emit_audit_event("inject_failure", "tamper_simulation", simulation_id, {"action": "inject_failure", "data": data or {}})
        return item

    def detect_tamper(self, simulation_id: str, data: dict | None = None) -> dict | None:
        """Action: Detect tamper."""
        item = self._store.get(simulation_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "detect_tamperd"
        emit_audit_event("detect_tamper", "tamper_simulation", simulation_id, {"action": "detect_tamper", "data": data or {}})
        return item

    def recover(self, simulation_id: str, data: dict | None = None) -> dict | None:
        """Action: Execute recovery."""
        item = self._store.get(simulation_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "recoverd"
        emit_audit_event("recover", "tamper_simulation", simulation_id, {"action": "recover", "data": data or {}})
        return item

    def simulation_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = TamperSimulationService()
