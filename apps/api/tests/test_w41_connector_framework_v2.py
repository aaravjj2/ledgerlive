"""Tests for Wave 41: Connector Framework 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w41_connector_framework_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w41_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w41_create(client):
    r = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "connector_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w41_list(client):
    await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    r = await client.get("/api/connectors-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w41_get_by_id(client):
    r = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    item_id = r.json()["connector_id"]
    r2 = await client.get(f"/api/connectors-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w41_get_not_found(client):
    r = await client.get("/api/connectors-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w41_configure(client):
    r = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    item_id = r.json()["connector_id"]
    r2 = await client.post(f"/api/connectors-v2/{item_id}/configure", json={})
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w41_sync_now(client):
    r = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    item_id = r.json()["connector_id"]
    r2 = await client.post(f"/api/connectors-v2/{item_id}/sync", json={})
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w41_test_connection(client):
    r = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    item_id = r.json()["connector_id"]
    r2 = await client.post(f"/api/connectors-v2/{item_id}/test", json={})
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w41_configure_not_found(client):
    r = await client.post("/api/connectors-v2/nonexistent-id/configure", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w41_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "connector_framework_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w41_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "connector_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w41_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/connectors-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w41_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/connectors-v2", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'capabilities': [], 'scopes': [], 'sync_schedule': 'test-sync_schedule', 'status': 'test-status', 'last_sync_at': 'test-last_sync_at', 'config': {}, 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["connector_id"]
    r2 = await client.get("/api/connectors-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/connectors-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["connector_id"] == item_id
