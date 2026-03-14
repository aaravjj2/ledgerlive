"""Tests for Wave 12: Authentication & RBAC

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w12_auth import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w12_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w12_create(client):
    r = await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    assert r.status_code == 201
    data = r.json()
    assert "user_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w12_list(client):
    await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    r = await client.get("/api/auth/users")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w12_get_by_id(client):
    r = await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    item_id = r.json()["user_id"]
    r2 = await client.get(f"/api/auth/users/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["user_id"] == item_id

@pytest.mark.asyncio
async def test_w12_get_not_found(client):
    r = await client.get("/api/auth/users/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w12_update(client):
    r = await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    item_id = r.json()["user_id"]
    r2 = await client.put(f"/api/auth/users/{item_id}/role", json={"name": "updated"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"

@pytest.mark.asyncio
async def test_w12_deactivate_user(client):
    r = await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    item_id = r.json()["user_id"]
    r2 = await client.post(f"/api/auth/users/{item_id}/deactivate", json={})
    assert r2.status_code == 200
    assert r2.json()["user_id"] == item_id

@pytest.mark.asyncio
async def test_w12_deactivate_user_not_found(client):
    r = await client.post("/api/auth/users/nonexistent-id/deactivate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w12_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "auth"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w12_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/auth/users", json={'email': 'test-email', 'role': 'test-role', 'tenant_id': 'test-tenant_id', 'active': True, 'last_login': 'test-last_login'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "user_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w12_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/auth/users", json={})
    assert r.status_code == 201
