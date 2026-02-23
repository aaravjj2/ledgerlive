"""Tests for Wave 105: Key Management 3.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w105_key_management import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w105_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w105_create(client):
    r = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "key_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w105_list(client):
    await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    r = await client.get("/api/key-management")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w105_get_by_id(client):
    r = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    item_id = r.json()["key_id"]
    r2 = await client.get(f"/api/key-management/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["key_id"] == item_id

@pytest.mark.asyncio
async def test_w105_get_not_found(client):
    r = await client.get("/api/key-management/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w105_rotate_key(client):
    r = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    item_id = r.json()["key_id"]
    r2 = await client.post(f"/api/key-management/{item_id}/rotate", json={})
    assert r2.status_code == 200
    assert r2.json()["key_id"] == item_id

@pytest.mark.asyncio
async def test_w105_verify_backward(client):
    r = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    item_id = r.json()["key_id"]
    r2 = await client.post(f"/api/key-management/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["key_id"] == item_id

@pytest.mark.asyncio
async def test_w105_rotate_key_not_found(client):
    r = await client.post("/api/key-management/nonexistent-id/rotate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w105_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "key_management"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w105_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "key_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w105_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/key-management", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w105_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/key-management", json={'key_type': 'test-key_type', 'algorithm': 'test-algorithm', 'version': 1, 'active': True, 'rotated_from': 'test-rotated_from', 'backward_verifiable': True, 'status': 'test-status', 'created_at': 'test-created_at', 'rotated_at': 'test-rotated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["key_id"]
    r2 = await client.get("/api/key-management")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/key-management/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["key_id"] == item_id
