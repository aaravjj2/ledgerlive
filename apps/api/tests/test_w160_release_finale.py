"""Tests for Wave 160: Release Finale

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w160_release_finale import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w160_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w160_create(client):
    r = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    assert r.status_code == 201
    data = r.json()
    assert "finale_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w160_list(client):
    await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    r = await client.get("/api/release-finales")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w160_get_by_id(client):
    r = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["finale_id"]
    r2 = await client.get(f"/api/release-finales/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["finale_id"] == item_id

@pytest.mark.asyncio
async def test_w160_get_not_found(client):
    r = await client.get("/api/release-finales/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w160_verify_finale(client):
    r = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["finale_id"]
    r2 = await client.post(f"/api/release-finales/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["finale_id"] == item_id

@pytest.mark.asyncio
async def test_w160_sign_finale(client):
    r = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["finale_id"]
    r2 = await client.post(f"/api/release-finales/{item_id}/sign", json={})
    assert r2.status_code == 200
    assert r2.json()["finale_id"] == item_id

@pytest.mark.asyncio
async def test_w160_verify_finale_not_found(client):
    r = await client.post("/api/release-finales/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w160_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "release_finale"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w160_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "finale_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w160_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/release-finales", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w160_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/release-finales", json={'release_version': 'test-release_version', 'proof_pack_ref': 'test-proof_pack_ref', 'all_tests_pass': True, 'all_gates_pass': True, 'determinism_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'finalized_at': 'test-finalized_at'})
    assert r1.status_code == 201
    item_id = r1.json()["finale_id"]
    r2 = await client.get("/api/release-finales")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/release-finales/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["finale_id"] == item_id
