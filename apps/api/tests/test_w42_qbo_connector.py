"""Tests for Wave 42: QuickBooks Online Connector

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w42_qbo_connector import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w42_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w42_create(client):
    r = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "sync_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w42_list(client):
    await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/qbo/syncs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w42_get_by_id(client):
    r = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["sync_id"]
    r2 = await client.get(f"/api/qbo/syncs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["sync_id"] == item_id

@pytest.mark.asyncio
async def test_w42_get_not_found(client):
    r = await client.get("/api/qbo/syncs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w42_retry_sync(client):
    r = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["sync_id"]
    r2 = await client.post(f"/api/qbo/syncs/{item_id}/retry", json={})
    assert r2.status_code == 200
    assert r2.json()["sync_id"] == item_id

@pytest.mark.asyncio
async def test_w42_cancel_sync(client):
    r = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["sync_id"]
    r2 = await client.post(f"/api/qbo/syncs/{item_id}/cancel", json={})
    assert r2.status_code == 200
    assert r2.json()["sync_id"] == item_id

@pytest.mark.asyncio
async def test_w42_retry_sync_not_found(client):
    r = await client.post("/api/qbo/syncs/nonexistent-id/retry", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w42_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "qbo_connector"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w42_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "sync_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w42_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/qbo/syncs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w42_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/qbo/syncs", json={'connector_id': 'test-connector_id', 'entity_type': 'test-entity_type', 'direction': 'test-direction', 'records_synced': 1, 'records_failed': 1, 'status': 'test-status', 'mock_mode': True, 'pagination_token': 'test-pagination_token', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["sync_id"]
    r2 = await client.get("/api/qbo/syncs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/qbo/syncs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["sync_id"] == item_id
