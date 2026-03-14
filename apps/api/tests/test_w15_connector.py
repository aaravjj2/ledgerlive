"""Tests for Wave 15: External Connector

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w15_connector import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w15_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w15_create(client):
    r = await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    assert r.status_code == 201
    data = r.json()
    assert "connector_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w15_list(client):
    await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    r = await client.get("/api/connectors")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w15_get_by_id(client):
    r = await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    item_id = r.json()["connector_id"]
    r2 = await client.get(f"/api/connectors/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w15_get_not_found(client):
    r = await client.get("/api/connectors/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w15_sync(client):
    r = await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    item_id = r.json()["connector_id"]
    r2 = await client.post(f"/api/connectors/{item_id}/sync", json={})
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w15_test_conn(client):
    r = await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    item_id = r.json()["connector_id"]
    r2 = await client.post(f"/api/connectors/{item_id}/test", json={})
    assert r2.status_code == 200
    assert r2.json()["connector_id"] == item_id

@pytest.mark.asyncio
async def test_w15_sync_not_found(client):
    r = await client.post("/api/connectors/nonexistent-id/sync", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w15_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "connector"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w15_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/connectors", json={'name': 'test-name', 'connector_type': 'test-connector_type', 'config': {}, 'status': 'test-status', 'last_sync': 'test-last_sync'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "connector_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w15_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/connectors", json={})
    assert r.status_code == 201
