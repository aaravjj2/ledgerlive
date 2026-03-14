"""Tests for Wave 29: Deploy Configuration

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w29_deploy_config import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w29_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w29_create(client):
    r = await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "config_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w29_list(client):
    await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    r = await client.get("/api/deploy/configs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w29_get_by_id(client):
    r = await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["config_id"]
    r2 = await client.get(f"/api/deploy/configs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["config_id"] == item_id

@pytest.mark.asyncio
async def test_w29_get_not_found(client):
    r = await client.get("/api/deploy/configs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w29_activate(client):
    r = await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["config_id"]
    r2 = await client.post(f"/api/deploy/configs/{item_id}/activate", json={})
    assert r2.status_code == 200
    assert r2.json()["config_id"] == item_id

@pytest.mark.asyncio
async def test_w29_validate_config(client):
    r = await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["config_id"]
    r2 = await client.post(f"/api/deploy/configs/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["config_id"] == item_id

@pytest.mark.asyncio
async def test_w29_activate_not_found(client):
    r = await client.post("/api/deploy/configs/nonexistent-id/activate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w29_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "deploy_config"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w29_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/deploy/configs", json={'environment': 'test-environment', 'region': 'test-region', 'settings': {}, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "config_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w29_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/deploy/configs", json={})
    assert r.status_code == 201
