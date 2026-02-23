"""Tests for Wave 126: Legal Holds + ABAC

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w126_legal_holds_abac import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w126_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w126_create(client):
    r = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    assert r.status_code == 201
    data = r.json()
    assert "hold_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w126_list(client):
    await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    r = await client.get("/api/legal-holds-abac")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w126_get_by_id(client):
    r = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    item_id = r.json()["hold_id"]
    r2 = await client.get(f"/api/legal-holds-abac/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["hold_id"] == item_id

@pytest.mark.asyncio
async def test_w126_get_not_found(client):
    r = await client.get("/api/legal-holds-abac/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w126_enforce(client):
    r = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    item_id = r.json()["hold_id"]
    r2 = await client.post(f"/api/legal-holds-abac/{item_id}/enforce", json={})
    assert r2.status_code == 200
    assert r2.json()["hold_id"] == item_id

@pytest.mark.asyncio
async def test_w126_release_hold(client):
    r = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    item_id = r.json()["hold_id"]
    r2 = await client.post(f"/api/legal-holds-abac/{item_id}/release", json={})
    assert r2.status_code == 200
    assert r2.json()["hold_id"] == item_id

@pytest.mark.asyncio
async def test_w126_enforce_not_found(client):
    r = await client.post("/api/legal-holds-abac/nonexistent-id/enforce", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w126_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "legal_holds_abac"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w126_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "hold_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w126_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/legal-holds-abac", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w126_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/legal-holds-abac", json={'matter_id': 'test-matter_id', 'abac_policy_id': 'test-abac_policy_id', 'scope': {}, 'enforced': True, 'override_denied': True, 'status': 'test-status', 'created_at': 'test-created_at', 'released_at': 'test-released_at'})
    assert r1.status_code == 201
    item_id = r1.json()["hold_id"]
    r2 = await client.get("/api/legal-holds-abac")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/legal-holds-abac/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["hold_id"] == item_id
