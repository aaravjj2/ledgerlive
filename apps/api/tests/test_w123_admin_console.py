"""Tests for Wave 123: Policy Admin Console

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w123_admin_console import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w123_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w123_create(client):
    r = await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "action_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w123_list(client):
    await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    r = await client.get("/api/admin-console")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w123_get_by_id(client):
    r = await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    item_id = r.json()["action_id"]
    r2 = await client.get(f"/api/admin-console/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w123_get_not_found(client):
    r = await client.get("/api/admin-console/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w123_revert_action(client):
    r = await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/admin-console/{item_id}/revert", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w123_revert_action_not_found(client):
    r = await client.post("/api/admin-console/nonexistent-id/revert", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w123_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "admin_console"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w123_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "action_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w123_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/admin-console", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w123_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/admin-console", json={'admin_user': 'test-admin_user', 'action_type': 'test-action_type', 'target_policy': 'test-target_policy', 'old_value': {}, 'new_value': {}, 'status': 'test-status', 'audit_trail_id': 'test-audit_trail_id', 'performed_at': 'test-performed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["action_id"]
    r2 = await client.get("/api/admin-console")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/admin-console/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["action_id"] == item_id
