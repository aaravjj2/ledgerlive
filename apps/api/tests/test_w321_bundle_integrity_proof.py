"""Tests for Wave 321: Bundle Integrity Proof v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w321_bundle_integrity_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w321_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w321_create(client):
    r = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "integrity_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w321_list(client):
    await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    r = await client.get("/api/bundle-integrity-proof")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w321_get_by_id(client):
    r = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    item_id = r.json()["integrity_id"]
    r2 = await client.get(f"/api/bundle-integrity-proof/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["integrity_id"] == item_id

@pytest.mark.asyncio
async def test_w321_get_not_found(client):
    r = await client.get("/api/bundle-integrity-proof/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w321_verify_signature(client):
    r = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    item_id = r.json()["integrity_id"]
    r2 = await client.post(f"/api/bundle-integrity-proof/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["integrity_id"] == item_id

@pytest.mark.asyncio
async def test_w321_tamper_test(client):
    r = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    item_id = r.json()["integrity_id"]
    r2 = await client.post(f"/api/bundle-integrity-proof/{item_id}/tamper-test", json={})
    assert r2.status_code == 200
    assert r2.json()["integrity_id"] == item_id

@pytest.mark.asyncio
async def test_w321_verify_signature_not_found(client):
    r = await client.post("/api/bundle-integrity-proof/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w321_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "bundle_integrity_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w321_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "integrity_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w321_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/bundle-integrity-proof", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w321_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/bundle-integrity-proof", json={'bundle_ref': 'test-bundle_ref', 'signature': 'test-signature', 'public_key_ref': 'test-public_key_ref', 'signed_hash': 'test-signed_hash', 'verified': True, 'tamper_detected': True, 'tamper_detail': 'test-tamper_detail', 'signer_identity': 'test-signer_identity', 'deterministic': True, 'status': 'test-status', 'signed_at': 'test-signed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["integrity_id"]
    r2 = await client.get("/api/bundle-integrity-proof")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/bundle-integrity-proof/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["integrity_id"] == item_id
