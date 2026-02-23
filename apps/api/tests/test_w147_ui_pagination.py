"""Tests for Wave 147: UI Pagination Determinism

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w147_ui_pagination import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w147_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w147_create(client):
    r = await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "test_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w147_list(client):
    await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/ui-pagination")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w147_get_by_id(client):
    r = await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["test_id"]
    r2 = await client.get(f"/api/ui-pagination/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w147_get_not_found(client):
    r = await client.get("/api/ui-pagination/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w147_verify_ordering(client):
    r = await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["test_id"]
    r2 = await client.post(f"/api/ui-pagination/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w147_verify_ordering_not_found(client):
    r = await client.post("/api/ui-pagination/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w147_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ui_pagination"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w147_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "test_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w147_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ui-pagination", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w147_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/ui-pagination", json={'endpoint': 'test-endpoint', 'page_count': 1, 'items_per_page': 1, 'ordering_stable': True, 'filter_deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["test_id"]
    r2 = await client.get("/api/ui-pagination")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ui-pagination/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["test_id"] == item_id
