"""Tests for Wave 106: Compliance Bundle Signing

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w106_compliance_signing import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w106_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w106_create(client):
    r = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "bundle_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w106_list(client):
    await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    r = await client.get("/api/compliance-signing")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w106_get_by_id(client):
    r = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.get(f"/api/compliance-signing/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w106_get_not_found(client):
    r = await client.get("/api/compliance-signing/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w106_sign_bundle(client):
    r = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/compliance-signing/{item_id}/sign", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w106_verify_tamper(client):
    r = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/compliance-signing/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w106_sign_bundle_not_found(client):
    r = await client.post("/api/compliance-signing/nonexistent-id/sign", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w106_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "compliance_signing"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w106_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "bundle_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w106_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/compliance-signing", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w106_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/compliance-signing", json={'bundle_type': 'test-bundle_type', 'content_hash': 'test-content_hash', 'signature': 'test-signature', 'signer_id': 'test-signer_id', 'tamper_verified': True, 'status': 'test-status', 'signed_at': 'test-signed_at', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["bundle_id"]
    r2 = await client.get("/api/compliance-signing")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/compliance-signing/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["bundle_id"] == item_id
