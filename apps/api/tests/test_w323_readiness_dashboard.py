"""Tests for Wave 323: Readiness Dashboard v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w323_readiness_dashboard import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w323_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w323_create(client):
    r = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "dashboard_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w323_list(client):
    await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/readiness-dashboard")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w323_get_by_id(client):
    r = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["dashboard_id"]
    r2 = await client.get(f"/api/readiness-dashboard/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["dashboard_id"] == item_id

@pytest.mark.asyncio
async def test_w323_get_not_found(client):
    r = await client.get("/api/readiness-dashboard/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w323_run_checklist(client):
    r = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["dashboard_id"]
    r2 = await client.post(f"/api/readiness-dashboard/{item_id}/check", json={})
    assert r2.status_code == 200
    assert r2.json()["dashboard_id"] == item_id

@pytest.mark.asyncio
async def test_w323_export_status(client):
    r = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["dashboard_id"]
    r2 = await client.post(f"/api/readiness-dashboard/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["dashboard_id"] == item_id

@pytest.mark.asyncio
async def test_w323_run_checklist_not_found(client):
    r = await client.post("/api/readiness-dashboard/nonexistent-id/check", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w323_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "readiness_dashboard"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w323_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "dashboard_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w323_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/readiness-dashboard", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w323_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/readiness-dashboard", json={'checklist_items': [], 'items_passed': 1, 'items_failed': 1, 'items_pending': 1, 'overall_ready': True, 'last_check_refs': {}, 'blocking_items': [], 'readiness_score': 1.0, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["dashboard_id"]
    r2 = await client.get("/api/readiness-dashboard")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/readiness-dashboard/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["dashboard_id"] == item_id
