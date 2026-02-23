"""Tests for Wave 212: Binder Regeneration From Replay

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w212_binder_regen import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w212_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w212_create(client):
    r = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "regen_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w212_list(client):
    await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    r = await client.get("/api/binder-regen")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w212_get_by_id(client):
    r = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    item_id = r.json()["regen_id"]
    r2 = await client.get(f"/api/binder-regen/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["regen_id"] == item_id

@pytest.mark.asyncio
async def test_w212_get_not_found(client):
    r = await client.get("/api/binder-regen/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w212_verify_identity(client):
    r = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    item_id = r.json()["regen_id"]
    r2 = await client.post(f"/api/binder-regen/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["regen_id"] == item_id

@pytest.mark.asyncio
async def test_w212_compare_hashes(client):
    r = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    item_id = r.json()["regen_id"]
    r2 = await client.post(f"/api/binder-regen/{item_id}/compare", json={})
    assert r2.status_code == 200
    assert r2.json()["regen_id"] == item_id

@pytest.mark.asyncio
async def test_w212_verify_identity_not_found(client):
    r = await client.post("/api/binder-regen/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w212_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "binder_regen"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w212_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "regen_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w212_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/binder-regen", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w212_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/binder-regen", json={'replay_id': 'test-replay_id', 'original_binder_hash': 'test-original_binder_hash', 'regen_binder_hash': 'test-regen_binder_hash', 'original_board_hash': 'test-original_board_hash', 'regen_board_hash': 'test-regen_board_hash', 'byte_identical': True, 'hash_match': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'regenerated_at': 'test-regenerated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["regen_id"]
    r2 = await client.get("/api/binder-regen")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/binder-regen/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["regen_id"] == item_id
