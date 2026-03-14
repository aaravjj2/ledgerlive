"""Tests for Wave 260: Security Proof Wave v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w260_security_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w260_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w260_create(client):
    r = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "proof_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w260_list(client):
    await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/security-proof")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w260_get_by_id(client):
    r = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.get(f"/api/security-proof/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w260_get_not_found(client):
    r = await client.get("/api/security-proof/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w260_verify_proof(client):
    r = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/security-proof/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w260_seal_proof(client):
    r = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/security-proof/{item_id}/seal", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w260_verify_proof_not_found(client):
    r = await client.post("/api/security-proof/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w260_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "security_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w260_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "proof_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w260_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/security-proof", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w260_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/security-proof", json={'blocked_action_ref': 'test-blocked_action_ref', 'security_event_ref': 'test-security_event_ref', 'fix_path_ref': 'test-fix_path_ref', 'approval_ref': 'test-approval_ref', 'proceed_result': 'test-proceed_result', 'posture_pack_ref': 'test-posture_pack_ref', 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'all_verified': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["proof_id"]
    r2 = await client.get("/api/security-proof")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/security-proof/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["proof_id"] == item_id
