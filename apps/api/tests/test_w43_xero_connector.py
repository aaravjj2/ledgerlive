"""Tests for Wave 43: Xero Connector

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w43_xero_connector import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w43_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w43_create(client):
    r = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "sync_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w43_list(client):
    await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/xero/syncs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w43_get_by_id(client):
    r = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["sync_id"]
    r2 = await client.get(f"/api/xero/syncs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["sync_id"] == item_id

@pytest.mark.asyncio
async def test_w43_get_not_found(client):
    r = await client.get("/api/xero/syncs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w43_retry_sync(client):
    r = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["sync_id"]
    r2 = await client.post(f"/api/xero/syncs/{item_id}/retry", json={})
    assert r2.status_code == 200
    assert r2.json()["sync_id"] == item_id

@pytest.mark.asyncio
async def test_w43_cancel_sync(client):
    r = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["sync_id"]
    r2 = await client.post(f"/api/xero/syncs/{item_id}/cancel", json={})
    assert r2.status_code == 200
    assert r2.json()["sync_id"] == item_id

@pytest.mark.asyncio
async def test_w43_retry_sync_not_found(client):
    r = await client.post("/api/xero/syncs/nonexistent-id/retry", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w43_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "xero_connector"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w43_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "sync_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w43_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/xero/syncs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w43_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/xero/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["sync_id"]
    r2 = await client.get("/api/xero/syncs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/xero/syncs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["sync_id"] == item_id
