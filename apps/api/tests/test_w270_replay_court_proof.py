"""Tests for Wave 270: Replay Court Proof Wave v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w270_replay_court_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w270_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w270_create(client):
    r = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "proof_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w270_list(client):
    await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/replay-court-proof")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w270_get_by_id(client):
    r = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.get(f"/api/replay-court-proof/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w270_get_not_found(client):
    r = await client.get("/api/replay-court-proof/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w270_verify_proof(client):
    r = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/replay-court-proof/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w270_seal_proof(client):
    r = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/replay-court-proof/{item_id}/seal", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w270_verify_proof_not_found(client):
    r = await client.post("/api/replay-court-proof/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w270_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "replay_court_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w270_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "proof_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w270_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/replay-court-proof", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w270_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/replay-court-proof", json={'rc_ref': 'test-rc_ref', 'court_pack_ref': 'test-court_pack_ref', 'replay_ref': 'test-replay_ref', 'binder_regen_ref': 'test-binder_regen_ref', 'hash_match_verified': True, 'all_steps_passed': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'evidence_bundle': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["proof_id"]
    r2 = await client.get("/api/replay-court-proof")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/replay-court-proof/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["proof_id"] == item_id
