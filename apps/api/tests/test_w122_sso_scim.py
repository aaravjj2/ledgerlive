"""Tests for Wave 122: SSO/SCIM Mock Contracts

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w122_sso_scim import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w122_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w122_create(client):
    r = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    assert r.status_code == 201
    data = r.json()
    assert "contract_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w122_list(client):
    await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    r = await client.get("/api/sso-scim")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w122_get_by_id(client):
    r = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    item_id = r.json()["contract_id"]
    r2 = await client.get(f"/api/sso-scim/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["contract_id"] == item_id

@pytest.mark.asyncio
async def test_w122_get_not_found(client):
    r = await client.get("/api/sso-scim/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w122_sync_users(client):
    r = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    item_id = r.json()["contract_id"]
    r2 = await client.post(f"/api/sso-scim/{item_id}/sync", json={})
    assert r2.status_code == 200
    assert r2.json()["contract_id"] == item_id

@pytest.mark.asyncio
async def test_w122_map_roles(client):
    r = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    item_id = r.json()["contract_id"]
    r2 = await client.post(f"/api/sso-scim/{item_id}/map-roles", json={})
    assert r2.status_code == 200
    assert r2.json()["contract_id"] == item_id

@pytest.mark.asyncio
async def test_w122_sync_users_not_found(client):
    r = await client.post("/api/sso-scim/nonexistent-id/sync", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w122_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "sso_scim"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w122_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "contract_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w122_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/sso-scim", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w122_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/sso-scim", json={'protocol': 'test-protocol', 'provider': 'test-provider', 'mock_mode': True, 'users_synced': 1, 'groups_synced': 1, 'role_mappings': {}, 'status': 'test-status', 'synced_at': 'test-synced_at'})
    assert r1.status_code == 201
    item_id = r1.json()["contract_id"]
    r2 = await client.get("/api/sso-scim")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/sso-scim/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["contract_id"] == item_id
