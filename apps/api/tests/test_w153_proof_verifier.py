"""Tests for Wave 153: Proof Pack Verifier

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w153_proof_verifier import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w153_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w153_create(client):
    r = await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "verifier_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w153_list(client):
    await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/proof-verifiers")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w153_get_by_id(client):
    r = await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verifier_id"]
    r2 = await client.get(f"/api/proof-verifiers/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["verifier_id"] == item_id

@pytest.mark.asyncio
async def test_w153_get_not_found(client):
    r = await client.get("/api/proof-verifiers/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w153_check_proof(client):
    r = await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verifier_id"]
    r2 = await client.post(f"/api/proof-verifiers/{item_id}/check", json={})
    assert r2.status_code == 200
    assert r2.json()["verifier_id"] == item_id

@pytest.mark.asyncio
async def test_w153_check_proof_not_found(client):
    r = await client.post("/api/proof-verifiers/nonexistent-id/check", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w153_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "proof_verifier"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w153_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "verifier_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w153_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/proof-verifiers", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w153_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/proof-verifiers", json={'proof_refs': [], 'all_exist': True, 'all_pass': True, 'missing_proofs': [], 'failed_proofs': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["verifier_id"]
    r2 = await client.get("/api/proof-verifiers")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/proof-verifiers/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["verifier_id"] == item_id
