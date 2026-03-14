"""Tests for Wave 129: Policy Proof Pack

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w129_policy_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w129_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w129_create(client):
    r = await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "proof_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w129_list(client):
    await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/policy-proofs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w129_get_by_id(client):
    r = await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.get(f"/api/policy-proofs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w129_get_not_found(client):
    r = await client.get("/api/policy-proofs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w129_verify_proof(client):
    r = await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/policy-proofs/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w129_verify_proof_not_found(client):
    r = await client.post("/api/policy-proofs/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w129_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "policy_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w129_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "proof_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w129_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/policy-proofs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w129_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/policy-proofs", json={'policy_matrix': {}, 'deny_logs': [], 'regression_results': [], 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["proof_id"]
    r2 = await client.get("/api/policy-proofs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/policy-proofs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["proof_id"] == item_id
