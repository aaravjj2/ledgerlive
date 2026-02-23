"""Tests for Wave 203: Exactly-Once Tool Effects v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w203_exactly_once import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w203_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w203_create(client):
    r = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "effect_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w203_list(client):
    await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/exactly-once")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w203_get_by_id(client):
    r = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["effect_id"]
    r2 = await client.get(f"/api/exactly-once/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["effect_id"] == item_id

@pytest.mark.asyncio
async def test_w203_get_not_found(client):
    r = await client.get("/api/exactly-once/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w203_verify_once(client):
    r = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["effect_id"]
    r2 = await client.post(f"/api/exactly-once/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["effect_id"] == item_id

@pytest.mark.asyncio
async def test_w203_hammer_test(client):
    r = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["effect_id"]
    r2 = await client.post(f"/api/exactly-once/{item_id}/hammer", json={})
    assert r2.status_code == 200
    assert r2.json()["effect_id"] == item_id

@pytest.mark.asyncio
async def test_w203_verify_once_not_found(client):
    r = await client.post("/api/exactly-once/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w203_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "exactly_once"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w203_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "effect_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w203_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/exactly-once", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w203_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/exactly-once", json={'tool_name': 'test-tool_name', 'idempotency_key': 'test-idempotency_key', 'close_period_id': 'test-close_period_id', 'mutation_count': 1, 'duplicate_attempts': 1, 'side_effect_ledger': [], 'ledger_hash': 'test-ledger_hash', 'exactly_once_verified': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["effect_id"]
    r2 = await client.get("/api/exactly-once")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/exactly-once/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["effect_id"] == item_id
