"""Tests for Wave 262: Court Pack v4

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w262_court_pack_v4 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w262_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w262_create(client):
    r = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "pack_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w262_list(client):
    await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/court-pack-v4")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w262_get_by_id(client):
    r = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.get(f"/api/court-pack-v4/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w262_get_not_found(client):
    r = await client.get("/api/court-pack-v4/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w262_verify_pack(client):
    r = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.post(f"/api/court-pack-v4/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w262_attach_parity(client):
    r = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.post(f"/api/court-pack-v4/{item_id}/parity", json={})
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w262_verify_pack_not_found(client):
    r = await client.post("/api/court-pack-v4/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w262_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "court_pack_v4"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w262_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "pack_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w262_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/court-pack-v4", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w262_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/court-pack-v4", json={'rc_ref': 'test-rc_ref', 'offline_viewer_data': {}, 'verify_script': 'test-verify_script', 'parity_report': {}, 'attachments': [], 'content_hash': 'test-content_hash', 'verification_result': 'test-verification_result', 'pack_size_bytes': 1, 'deterministic': True, 'generated_from': 'test-generated_from', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["pack_id"]
    r2 = await client.get("/api/court-pack-v4")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/court-pack-v4/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["pack_id"] == item_id
