"""Tests for Wave 2: Entity Management

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w02_entity import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w02_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w02_create(client):
    r = await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    assert r.status_code == 201
    data = r.json()
    assert "entity_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w02_list(client):
    await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    r = await client.get("/api/entities")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w02_get_by_id(client):
    r = await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    item_id = r.json()["entity_id"]
    r2 = await client.get(f"/api/entities/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["entity_id"] == item_id

@pytest.mark.asyncio
async def test_w02_get_not_found(client):
    r = await client.get("/api/entities/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w02_update(client):
    r = await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    item_id = r.json()["entity_id"]
    r2 = await client.put(f"/api/entities/{item_id}", json={"name": "updated"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"

@pytest.mark.asyncio
async def test_w02_deactivate(client):
    r = await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    item_id = r.json()["entity_id"]
    r2 = await client.post(f"/api/entities/{item_id}/deactivate", json={})
    assert r2.status_code == 200
    assert r2.json()["entity_id"] == item_id

@pytest.mark.asyncio
async def test_w02_deactivate_not_found(client):
    r = await client.post("/api/entities/nonexistent-id/deactivate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w02_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "entity"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w02_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/entities", json={'name': 'test-name', 'code': 'test-code', 'currency': 'test-currency', 'active': True})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "entity_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w02_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/entities", json={})
    assert r.status_code == 201
