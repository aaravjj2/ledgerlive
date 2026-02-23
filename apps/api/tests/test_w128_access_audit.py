"""Tests for Wave 128: Access Change Audit

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w128_access_audit import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w128_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w128_create(client):
    r = await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "audit_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w128_list(client):
    await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    r = await client.get("/api/access-audits")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w128_get_by_id(client):
    r = await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    item_id = r.json()["audit_id"]
    r2 = await client.get(f"/api/access-audits/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["audit_id"] == item_id

@pytest.mark.asyncio
async def test_w128_get_not_found(client):
    r = await client.get("/api/access-audits/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w128_revert_change(client):
    r = await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    item_id = r.json()["audit_id"]
    r2 = await client.post(f"/api/access-audits/{item_id}/revert", json={})
    assert r2.status_code == 200
    assert r2.json()["audit_id"] == item_id

@pytest.mark.asyncio
async def test_w128_revert_change_not_found(client):
    r = await client.post("/api/access-audits/nonexistent-id/revert", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w128_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "access_audit"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w128_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "audit_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w128_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/access-audits", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w128_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/access-audits", json={'user_id': 'test-user_id', 'change_type': 'test-change_type', 'old_permissions': {}, 'new_permissions': {}, 'changed_by': 'test-changed_by', 'reason': 'test-reason', 'status': 'test-status', 'changed_at': 'test-changed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["audit_id"]
    r2 = await client.get("/api/access-audits")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/access-audits/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["audit_id"] == item_id
