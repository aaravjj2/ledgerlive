"""Tests for Wave 221: Close Calendar Manager v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w221_close_calendar import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w221_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w221_create(client):
    r = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "calendar_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w221_list(client):
    await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/period-calendar")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w221_get_by_id(client):
    r = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["calendar_id"]
    r2 = await client.get(f"/api/period-calendar/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["calendar_id"] == item_id

@pytest.mark.asyncio
async def test_w221_get_not_found(client):
    r = await client.get("/api/period-calendar/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w221_advance_day(client):
    r = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["calendar_id"]
    r2 = await client.post(f"/api/period-calendar/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["calendar_id"] == item_id

@pytest.mark.asyncio
async def test_w221_set_milestone(client):
    r = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["calendar_id"]
    r2 = await client.post(f"/api/period-calendar/{item_id}/milestone", json={})
    assert r2.status_code == 200
    assert r2.json()["calendar_id"] == item_id

@pytest.mark.asyncio
async def test_w221_finalize_period(client):
    r = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["calendar_id"]
    r2 = await client.post(f"/api/period-calendar/{item_id}/finalize", json={})
    assert r2.status_code == 200
    assert r2.json()["calendar_id"] == item_id

@pytest.mark.asyncio
async def test_w221_advance_day_not_found(client):
    r = await client.post("/api/period-calendar/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w221_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "close_calendar"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w221_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "calendar_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w221_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/period-calendar", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w221_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/period-calendar", json={'period_name': 'test-period_name', 'fiscal_year': 1, 'fiscal_month': 1, 'open_date': 'test-open_date', 'target_close_date': 'test-target_close_date', 'actual_close_date': 'test-actual_close_date', 'working_days_remaining': 1, 'milestones': [], 'holiday_calendar': 'test-holiday_calendar', 'recurrence_rule': 'test-recurrence_rule', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["calendar_id"]
    r2 = await client.get("/api/period-calendar")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/period-calendar/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["calendar_id"] == item_id
