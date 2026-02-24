"""Tests for Wave 248: Channel Action Integration v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w248_channel_action_int import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w248_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w248_create(client):
    r = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    assert r.status_code == 201
    data = r.json()
    assert "channel_action_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w248_list(client):
    await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    r = await client.get("/api/channel-action")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w248_get_by_id(client):
    r = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    item_id = r.json()["channel_action_id"]
    r2 = await client.get(f"/api/channel-action/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["channel_action_id"] == item_id

@pytest.mark.asyncio
async def test_w248_get_not_found(client):
    r = await client.get("/api/channel-action/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w248_approve_via_channel(client):
    r = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    item_id = r.json()["channel_action_id"]
    r2 = await client.post(f"/api/channel-action/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["channel_action_id"] == item_id

@pytest.mark.asyncio
async def test_w248_deny_via_channel(client):
    r = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    item_id = r.json()["channel_action_id"]
    r2 = await client.post(f"/api/channel-action/{item_id}/deny", json={})
    assert r2.status_code == 200
    assert r2.json()["channel_action_id"] == item_id

@pytest.mark.asyncio
async def test_w248_approve_via_channel_not_found(client):
    r = await client.post("/api/channel-action/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w248_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "channel_action_int"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w248_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "channel_action_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w248_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/channel-action", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w248_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/channel-action", json={'channel_type': 'test-channel_type', 'card_ref': 'test-card_ref', 'action_type': 'test-action_type', 'plan_ref': 'test-plan_ref', 'step_ref': 'test-step_ref', 'decision': 'test-decision', 'decision_reason': 'test-decision_reason', 'decided_by': 'test-decided_by', 'plan_state_before': {}, 'plan_state_after': {}, 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'decided_at': 'test-decided_at'})
    assert r1.status_code == 201
    item_id = r1.json()["channel_action_id"]
    r2 = await client.get("/api/channel-action")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/channel-action/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["channel_action_id"] == item_id
