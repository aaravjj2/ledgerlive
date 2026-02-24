"""Tests for Wave 264: Reproduce Close v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w264_reproduce_close import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w264_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w264_create(client):
    r = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    assert r.status_code == 201
    data = r.json()
    assert "reproduce_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w264_list(client):
    await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    r = await client.get("/api/reproduce-close")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w264_get_by_id(client):
    r = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    item_id = r.json()["reproduce_id"]
    r2 = await client.get(f"/api/reproduce-close/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["reproduce_id"] == item_id

@pytest.mark.asyncio
async def test_w264_get_not_found(client):
    r = await client.get("/api/reproduce-close/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w264_verify_hashes(client):
    r = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    item_id = r.json()["reproduce_id"]
    r2 = await client.post(f"/api/reproduce-close/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["reproduce_id"] == item_id

@pytest.mark.asyncio
async def test_w264_regenerate_binder(client):
    r = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    item_id = r.json()["reproduce_id"]
    r2 = await client.post(f"/api/reproduce-close/{item_id}/regenerate", json={})
    assert r2.status_code == 200
    assert r2.json()["reproduce_id"] == item_id

@pytest.mark.asyncio
async def test_w264_verify_hashes_not_found(client):
    r = await client.post("/api/reproduce-close/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w264_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "reproduce_close"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w264_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "reproduce_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w264_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/reproduce-close", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w264_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/reproduce-close", json={'rc_ref': 'test-rc_ref', 'replay_ref': 'test-replay_ref', 'original_binder_hash': 'test-original_binder_hash', 'reproduced_binder_hash': 'test-reproduced_binder_hash', 'hashes_match': True, 'divergence_log': [], 'board_pack_ref': 'test-board_pack_ref', 'reproduced_board_hash': 'test-reproduced_board_hash', 'byte_identical': True, 'gate_result': 'test-gate_result', 'status': 'test-status', 'reproduced_at': 'test-reproduced_at'})
    assert r1.status_code == 201
    item_id = r1.json()["reproduce_id"]
    r2 = await client.get("/api/reproduce-close")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/reproduce-close/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["reproduce_id"] == item_id
