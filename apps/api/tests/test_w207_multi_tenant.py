"""Tests for Wave 207: Multi-Tenant Live Sessions v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w207_multi_tenant import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w207_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w207_create(client):
    r = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "tenant_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w207_list(client):
    await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/multi-tenant")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w207_get_by_id(client):
    r = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["tenant_id"]
    r2 = await client.get(f"/api/multi-tenant/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["tenant_id"] == item_id

@pytest.mark.asyncio
async def test_w207_get_not_found(client):
    r = await client.get("/api/multi-tenant/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w207_verify_isolation(client):
    r = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["tenant_id"]
    r2 = await client.post(f"/api/multi-tenant/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["tenant_id"] == item_id

@pytest.mark.asyncio
async def test_w207_test_cross_access(client):
    r = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["tenant_id"]
    r2 = await client.post(f"/api/multi-tenant/{item_id}/cross-access", json={})
    assert r2.status_code == 200
    assert r2.json()["tenant_id"] == item_id

@pytest.mark.asyncio
async def test_w207_verify_isolation_not_found(client):
    r = await client.post("/api/multi-tenant/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w207_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "multi_tenant"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w207_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "tenant_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w207_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/multi-tenant", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w207_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/multi-tenant", json={'workspace_id': 'test-workspace_id', 'session_id': 'test-session_id', 'owner_role': 'test-owner_role', 'access_policy': {}, 'isolation_verified': True, 'cross_tenant_blocked': True, 'blocked_attempts': [], 'rbac_result': 'test-rbac_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["tenant_id"]
    r2 = await client.get("/api/multi-tenant")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/multi-tenant/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["tenant_id"] == item_id
