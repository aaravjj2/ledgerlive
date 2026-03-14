"""Wave 221: Close Calendar Manager v1 — Manages financial close calendars with period definitions, milestone dates, and working-day calculations. Supports recurring close schedules and holiday-aware date math.

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class CloseCalendarService:
    """Domain service for Close Calendar Manager v1."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def _template(self) -> dict:
        return {
        "calendar_id": "",
        "period_name": "",
        "fiscal_year": 0,
        "fiscal_month": 0,
        "open_date": "",
        "target_close_date": "",
        "actual_close_date": "",
        "working_days_remaining": 0,
        "milestones": [],
        "holiday_calendar": "",
        "recurrence_rule": "",
        "status": "",
        "created_at": "",
        }

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)

    def list_calendars(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]

    def create_calendar(self, data: dict) -> dict:
        """Create/run: Create close calendar period."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {**self._template(), **data, "calendar_id": item_id}
        self._store[item_id] = item
        emit_audit_event("create_calendar", "close_calendar", item_id, {"data": data})
        return item

    def get_calendar(self, calendar_id: str) -> dict | None:
        """Get item by ID."""
        return self._store.get(calendar_id)

    def advance_day(self, calendar_id: str, data: dict | None = None) -> dict | None:
        """Action: Advance working day."""
        item = self._store.get(calendar_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "advance_dayd"
        emit_audit_event("advance_day", "close_calendar", calendar_id, {"action": "advance_day", "data": data or {}})
        return item

    def set_milestone(self, calendar_id: str, data: dict | None = None) -> dict | None:
        """Action: Set milestone date."""
        item = self._store.get(calendar_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "set_milestoned"
        emit_audit_event("set_milestone", "close_calendar", calendar_id, {"action": "set_milestone", "data": data or {}})
        return item

    def finalize_period(self, calendar_id: str, data: dict | None = None) -> dict | None:
        """Action: Finalize close period."""
        item = self._store.get(calendar_id)
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "finalize_periodd"
        emit_audit_event("finalize_period", "close_calendar", calendar_id, {"action": "finalize_period", "data": data or {}})
        return item

    def calendar_report(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]


# Module-level singleton
service = CloseCalendarService()
