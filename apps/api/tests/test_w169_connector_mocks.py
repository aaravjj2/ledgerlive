"""Tests for Wave 169: Connector Mock Servers v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w169_connector_mocks import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w169_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w169_create(client):
    r = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "mock_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w169_list(client):
    await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/connector-mocks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w169_get_by_id(client):
    r = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["mock_id"]
    r2 = await client.get(f"/api/connector-mocks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["mock_id"] == item_id

@pytest.mark.asyncio
async def test_w169_get_not_found(client):
    r = await client.get("/api/connector-mocks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w169_toggle_error(client):
    r = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["mock_id"]
    r2 = await client.post(f"/api/connector-mocks/{item_id}/toggle-error", json={})
    assert r2.status_code == 200
    assert r2.json()["mock_id"] == item_id

@pytest.mark.asyncio
async def test_w169_sync_mock(client):
    r = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["mock_id"]
    r2 = await client.post(f"/api/connector-mocks/{item_id}/sync", json={})
    assert r2.status_code == 200
    assert r2.json()["mock_id"] == item_id

@pytest.mark.asyncio
async def test_w169_toggle_error_not_found(client):
    r = await client.post("/api/connector-mocks/nonexistent-id/toggle-error", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w169_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "connector_mocks"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w169_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "mock_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w169_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/connector-mocks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w169_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/connector-mocks", json={'provider': 'test-provider', 'mock_type': 'test-mock_type', 'endpoint': 'test-endpoint', 'response_mode': 'test-response_mode', 'pagination_enabled': True, 'token_refresh_sim': True, 'error_rate_pct': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["mock_id"]
    r2 = await client.get("/api/connector-mocks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/connector-mocks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["mock_id"] == item_id
