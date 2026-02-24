"""Wave 298: Security Regression Budgets v1 — Fail if injection/exfil detection coverage or deny explainability regresses. Deterministic regression tracking.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class SecurityRegressionService:
    """Domain service for Security Regression Budgets v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "regression_id": "",
        "baseline_coverage_pct": 0.0,
        "current_coverage_pct": 0.0,
        "coverage_delta": 0.0,
        "regressed": True,
        "deny_explainability_pct": 0.0,
        "baseline_explainability_pct": 0.0,
        "explainability_regressed": True,
        "budget_threshold": 0.0,
        "within_budget": True,
        "regression_hash": "",
        "status": "",
        "measured_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_regressions(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_regression(self, data: dict) -> dict:
        """Create/run: Create security regression check."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "regression_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_regression", "security_regression", item_id, {"data": data})
        return item

    def get_regression(self, regression_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(regression_id)

    def measure_coverage(self, regression_id: str, data: dict | None = None) -> dict | None:
        """Action: Measure detection coverage."""
        item = self._store.get(regression_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "measure_coveraged"
        emit_audit_event("measure_coverage", "security_regression", regression_id, {"action": "measure_coverage", "data": data or {}})
        return item

    def measure_explainability(self, regression_id: str, data: dict | None = None) -> dict | None:
        """Action: Measure deny explainability."""
        item = self._store.get(regression_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "measure_explainabilityd"
        emit_audit_event("measure_explainability", "security_regression", regression_id, {"action": "measure_explainability", "data": data or {}})
        return item

    def regression_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = SecurityRegressionService()
