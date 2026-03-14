"""Tests for Wave 235: RC Automation Rules v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w235_rc_rules import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w235_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w235_create(client):
    r = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "rule_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w235_list(client):
    await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/rc-rules")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w235_get_by_id(client):
    r = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.get(f"/api/rc-rules/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w235_get_not_found(client):
    r = await client.get("/api/rc-rules/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w235_trigger_rule(client):
    r = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/rc-rules/{item_id}/trigger", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w235_toggle_rule(client):
    r = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/rc-rules/{item_id}/toggle", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w235_trigger_rule_not_found(client):
    r = await client.post("/api/rc-rules/nonexistent-id/trigger", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w235_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_rules"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w235_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "rule_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w235_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-rules", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w235_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-rules", json={'rule_name': 'test-rule_name', 'condition_type': 'test-condition_type', 'condition_params': {}, 'action_type': 'test-action_type', 'action_params': {}, 'enabled': True, 'trigger_count': 1, 'last_triggered_at': 'test-last_triggered_at', 'cooldown_s': 1, 'priority': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["rule_id"]
    r2 = await client.get("/api/rc-rules")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-rules/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["rule_id"] == item_id
