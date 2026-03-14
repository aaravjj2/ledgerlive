"""Tests for Wave 24: Data Retention

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w24_retention import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w24_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w24_create(client):
    r = await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    assert r.status_code == 201
    data = r.json()
    assert "policy_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w24_list(client):
    await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    r = await client.get("/api/retention/policies")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w24_get_by_id(client):
    r = await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    item_id = r.json()["policy_id"]
    r2 = await client.get(f"/api/retention/policies/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w24_get_not_found(client):
    r = await client.get("/api/retention/policies/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w24_run_policy(client):
    r = await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    item_id = r.json()["policy_id"]
    r2 = await client.post(f"/api/retention/policies/{item_id}/run", json={})
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w24_preview(client):
    r = await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    item_id = r.json()["policy_id"]
    r2 = await client.post(f"/api/retention/policies/{item_id}/preview", json={})
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w24_run_policy_not_found(client):
    r = await client.post("/api/retention/policies/nonexistent-id/run", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w24_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "retention"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w24_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/retention/policies", json={'name': 'test-name', 'entity_type': 'test-entity_type', 'retention_days': 1, 'action': 'test-action', 'active': True, 'last_run': 'test-last_run'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "policy_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w24_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/retention/policies", json={})
    assert r.status_code == 201
