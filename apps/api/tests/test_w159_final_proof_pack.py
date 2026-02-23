"""Tests for Wave 159: Final Proof of Proofs

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w159_final_proof_pack import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w159_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w159_create(client):
    r = await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "final_proof_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w159_list(client):
    await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/final-proof-packs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w159_get_by_id(client):
    r = await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["final_proof_id"]
    r2 = await client.get(f"/api/final-proof-packs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["final_proof_id"] == item_id

@pytest.mark.asyncio
async def test_w159_get_not_found(client):
    r = await client.get("/api/final-proof-packs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w159_verify_proof(client):
    r = await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["final_proof_id"]
    r2 = await client.post(f"/api/final-proof-packs/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["final_proof_id"] == item_id

@pytest.mark.asyncio
async def test_w159_verify_proof_not_found(client):
    r = await client.post("/api/final-proof-packs/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w159_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "final_proof_pack"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w159_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "final_proof_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w159_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/final-proof-packs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w159_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/final-proof-packs", json={'phase_proofs': [], 'total_waves': 1, 'total_tests': 1, 'all_gates_pass': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["final_proof_id"]
    r2 = await client.get("/api/final-proof-packs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/final-proof-packs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["final_proof_id"] == item_id
