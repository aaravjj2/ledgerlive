"""Tests for Wave 258: Security Posture Pack v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w258_security_posture_pack import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w258_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w258_create(client):
    r = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r.status_code == 201
    data = r.json()
    assert "pack_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w258_list(client):
    await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    r = await client.get("/api/security-posture-pack")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w258_get_by_id(client):
    r = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.get(f"/api/security-posture-pack/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w258_get_not_found(client):
    r = await client.get("/api/security-posture-pack/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w258_verify_pack(client):
    r = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.post(f"/api/security-posture-pack/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w258_sign_pack(client):
    r = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["pack_id"]
    r2 = await client.post(f"/api/security-posture-pack/{item_id}/sign", json={})
    assert r2.status_code == 200
    assert r2.json()["pack_id"] == item_id

@pytest.mark.asyncio
async def test_w258_verify_pack_not_found(client):
    r = await client.post("/api/security-posture-pack/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w258_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "security_posture_pack"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w258_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "pack_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w258_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/security-posture-pack", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w258_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/security-posture-pack", json={'events_snapshot': [], 'proofs_snapshot': [], 'verifier_outputs': [], 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'byte_identical': True, 'export_format': 'test-export_format', 'pack_size_bytes': 1, 'verification_status': 'test-verification_status', 'determinism_verified': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r1.status_code == 201
    item_id = r1.json()["pack_id"]
    r2 = await client.get("/api/security-posture-pack")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/security-posture-pack/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["pack_id"] == item_id
