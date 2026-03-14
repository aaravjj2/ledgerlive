"""Tests for Wave 78: Close KPI Scorecard

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w078_close_scorecard import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w078_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w078_create(client):
    r = await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "scorecard_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w078_list(client):
    await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    r = await client.get("/api/close-scorecards")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w078_get_by_id(client):
    r = await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["scorecard_id"]
    r2 = await client.get(f"/api/close-scorecards/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["scorecard_id"] == item_id

@pytest.mark.asyncio
async def test_w078_get_not_found(client):
    r = await client.get("/api/close-scorecards/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w078_drill_down(client):
    r = await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["scorecard_id"]
    r2 = await client.post(f"/api/close-scorecards/{item_id}/drilldown", json={})
    assert r2.status_code == 200
    assert r2.json()["scorecard_id"] == item_id

@pytest.mark.asyncio
async def test_w078_drill_down_not_found(client):
    r = await client.post("/api/close-scorecards/nonexistent-id/drilldown", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w078_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "close_scorecard"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w078_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "scorecard_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w078_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/close-scorecards", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w078_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/close-scorecards", json={'period_id': 'test-period_id', 'coverage_pct': 1.0, 'exceptions_count': 1, 'approvals_count': 1, 'timeliness_score': 1.0, 'overall_score': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["scorecard_id"]
    r2 = await client.get("/api/close-scorecards")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/close-scorecards/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["scorecard_id"] == item_id
