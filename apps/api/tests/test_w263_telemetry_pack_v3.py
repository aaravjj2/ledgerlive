"""Tests for Wave 263: Telemetry Pack v3

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w263_telemetry_pack_v3 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w263_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w263_create(client):
    r = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    assert r.status_code == 201
    data = r.json()
    assert "pack_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w263_list(client):
    await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    r = await client.get("/api/telemetry-pack-v3")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w263_get_by_id(client):
    r = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.get(f"/api/telemetry-pack-v3/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w263_get_not_found(client):
    r = await client.get("/api/telemetry-pack-v3/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w263_verify_pack(client):
    r = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.post(f"/api/telemetry-pack-v3/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w263_add_component(client):
    r = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.post(f"/api/telemetry-pack-v3/{item_id}/component", json={})
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w263_verify_pack_not_found(client):
    r = await client.post("/api/telemetry-pack-v3/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w263_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "telemetry_pack_v3"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w263_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "pack_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w263_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/telemetry-pack-v3", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w263_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/telemetry-pack-v3", json={'tool_trace_data': [], 'verifier_checks': [], 'drift_snapshot': {}, 'incidents_data': [], 'security_timeline_data': [], 'content_hash': 'test-content_hash', 'pack_format': 'test-pack_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'deterministic': True, 'status': 'test-status', 'assembled_at': 'test-assembled_at'})
    assert r1.status_code == 201
    item_id = r1.json()["pack_id"]
    r2 = await client.get("/api/telemetry-pack-v3")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/telemetry-pack-v3/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["pack_id"] == item_id
