"""Tests for Wave 133: Proof of Proof of Proof

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w133_proof_of_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w133_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w133_create(client):
    r = await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "pop_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w133_list(client):
    await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/proof-of-proof")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w133_get_by_id(client):
    r = await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["pop_id"]
    r2 = await client.get(f"/api/proof-of-proof/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["pop_id"] == item_id

@pytest.mark.asyncio
async def test_w133_get_not_found(client):
    r = await client.get("/api/proof-of-proof/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w133_verify_match(client):
    r = await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["pop_id"]
    r2 = await client.post(f"/api/proof-of-proof/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["pop_id"] == item_id

@pytest.mark.asyncio
async def test_w133_verify_match_not_found(client):
    r = await client.post("/api/proof-of-proof/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w133_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "proof_of_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w133_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "pop_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w133_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/proof-of-proof", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w133_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/proof-of-proof", json={'proof_run_1_hash': 'test-proof_run_1_hash', 'proof_run_2_hash': 'test-proof_run_2_hash', 'hashes_match': True, 'diffs': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["pop_id"]
    r2 = await client.get("/api/proof-of-proof")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/proof-of-proof/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["pop_id"] == item_id
