"""Tests for Wave 229: Race Control State Machine v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w229_rc_state_machine import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w229_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w229_create(client):
    r = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "machine_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w229_list(client):
    await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/rc-state-machine")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w229_get_by_id(client):
    r = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["machine_id"]
    r2 = await client.get(f"/api/rc-state-machine/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["machine_id"] == item_id

@pytest.mark.asyncio
async def test_w229_get_not_found(client):
    r = await client.get("/api/rc-state-machine/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w229_transition(client):
    r = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["machine_id"]
    r2 = await client.post(f"/api/rc-state-machine/{item_id}/transition", json={})
    assert r2.status_code == 200
    assert r2.json()["machine_id"] == item_id

@pytest.mark.asyncio
async def test_w229_lock_state(client):
    r = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["machine_id"]
    r2 = await client.post(f"/api/rc-state-machine/{item_id}/lock", json={})
    assert r2.status_code == 200
    assert r2.json()["machine_id"] == item_id

@pytest.mark.asyncio
async def test_w229_transition_not_found(client):
    r = await client.post("/api/rc-state-machine/nonexistent-id/transition", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w229_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_state_machine"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w229_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "machine_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w229_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-state-machine", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w229_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-state-machine", json={'period_id': 'test-period_id', 'current_state': 'test-current_state', 'previous_state': 'test-previous_state', 'valid_transitions': [], 'transition_history': [], 'guard_results': {}, 'last_transition_at': 'test-last_transition_at', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["machine_id"]
    r2 = await client.get("/api/rc-state-machine")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-state-machine/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["machine_id"] == item_id
