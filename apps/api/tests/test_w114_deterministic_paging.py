"""Tests for Wave 114: Deterministic Pagination

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w114_deterministic_paging import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w114_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w114_create(client):
    r = await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "page_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w114_list(client):
    await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/deterministic-paging")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w114_get_by_id(client):
    r = await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["page_id"]
    r2 = await client.get(f"/api/deterministic-paging/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["page_id"] == item_id

@pytest.mark.asyncio
async def test_w114_get_not_found(client):
    r = await client.get("/api/deterministic-paging/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w114_verify_order(client):
    r = await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["page_id"]
    r2 = await client.post(f"/api/deterministic-paging/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["page_id"] == item_id

@pytest.mark.asyncio
async def test_w114_verify_order_not_found(client):
    r = await client.post("/api/deterministic-paging/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w114_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "deterministic_paging"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w114_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "page_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w114_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/deterministic-paging", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w114_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/deterministic-paging", json={'endpoint': 'test-endpoint', 'page_number': 1, 'page_size': 1, 'total_items': 1, 'order_hash': 'test-order_hash', 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["page_id"]
    r2 = await client.get("/api/deterministic-paging")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/deterministic-paging/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["page_id"] == item_id
