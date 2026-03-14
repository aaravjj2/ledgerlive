"""Tests for Wave 44: Plaid Connector

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w44_plaid_connector import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w44_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w44_create(client):
    r = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    assert r.status_code == 201
    data = r.json()
    assert "feed_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w44_list(client):
    await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    r = await client.get("/api/plaid/feeds")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w44_get_by_id(client):
    r = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    item_id = r.json()["feed_id"]
    r2 = await client.get(f"/api/plaid/feeds/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["feed_id"] == item_id

@pytest.mark.asyncio
async def test_w44_get_not_found(client):
    r = await client.get("/api/plaid/feeds/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w44_sync_transactions(client):
    r = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    item_id = r.json()["feed_id"]
    r2 = await client.post(f"/api/plaid/feeds/{item_id}/sync", json={})
    assert r2.status_code == 200
    assert r2.json()["feed_id"] == item_id

@pytest.mark.asyncio
async def test_w44_dedupe(client):
    r = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    item_id = r.json()["feed_id"]
    r2 = await client.post(f"/api/plaid/feeds/{item_id}/dedupe", json={})
    assert r2.status_code == 200
    assert r2.json()["feed_id"] == item_id

@pytest.mark.asyncio
async def test_w44_enrich(client):
    r = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    item_id = r.json()["feed_id"]
    r2 = await client.post(f"/api/plaid/feeds/{item_id}/enrich", json={})
    assert r2.status_code == 200
    assert r2.json()["feed_id"] == item_id

@pytest.mark.asyncio
async def test_w44_sync_transactions_not_found(client):
    r = await client.post("/api/plaid/feeds/nonexistent-id/sync", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w44_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "plaid_connector"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w44_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "feed_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w44_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/plaid/feeds", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w44_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/plaid/feeds", json={'institution_id': 'test-institution_id', 'account_id': 'test-account_id', 'transactions_synced': 1, 'duplicates_skipped': 1, 'status': 'test-status', 'mock_mode': True, 'cursor': 'test-cursor', 'enrichment_applied': True, 'synced_at': 'test-synced_at'})
    assert r1.status_code == 201
    item_id = r1.json()["feed_id"]
    r2 = await client.get("/api/plaid/feeds")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/plaid/feeds/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["feed_id"] == item_id
