"""Tests for Wave 313: Atlassian Routing Rules v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w313_atlassian_routing import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w313_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w313_create(client):
    r = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "rule_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w313_list(client):
    await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/atlassian-routing")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w313_get_by_id(client):
    r = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.get(f"/api/atlassian-routing/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w313_get_not_found(client):
    r = await client.get("/api/atlassian-routing/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w313_trigger_rule(client):
    r = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/atlassian-routing/{item_id}/trigger", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w313_test_rule(client):
    r = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/atlassian-routing/{item_id}/test", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w313_trigger_rule_not_found(client):
    r = await client.post("/api/atlassian-routing/nonexistent-id/trigger", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w313_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "atlassian_routing"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w313_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "rule_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w313_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/atlassian-routing", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w313_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/atlassian-routing", json={'event_type': 'test-event_type', 'target_system': 'test-target_system', 'target_action': 'test-target_action', 'sla_hours': 1, 'escalation_enabled': True, 'frozen_time_ref': 'test-frozen_time_ref', 'conditions': [], 'priority_map': {}, 'last_triggered': 'test-last_triggered', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["rule_id"]
    r2 = await client.get("/api/atlassian-routing")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/atlassian-routing/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["rule_id"] == item_id
