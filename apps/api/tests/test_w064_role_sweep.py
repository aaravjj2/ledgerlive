"""Tests for Wave 64: Role Sweep E2E

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w064_role_sweep import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w064_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w064_create(client):
    r = await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "check_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w064_list(client):
    await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    r = await client.get("/api/role-sweeps")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w064_get_by_id(client):
    r = await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    item_id = r.json()["check_id"]
    r2 = await client.get(f"/api/role-sweeps/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["check_id"] == item_id

@pytest.mark.asyncio
async def test_w064_get_not_found(client):
    r = await client.get("/api/role-sweeps/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w064_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "role_sweep"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w064_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "check_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w064_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/role-sweeps", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w064_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/role-sweeps", json={'role': 'test-role', 'action': 'test-action', 'resource': 'test-resource', 'expected_result': 'test-expected_result', 'actual_result': 'test-actual_result', 'audit_logged': True, 'passed': True, 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["check_id"]
    r2 = await client.get("/api/role-sweeps")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/role-sweeps/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["check_id"] == item_id
