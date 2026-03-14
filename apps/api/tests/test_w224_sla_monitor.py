"""Tests for Wave 224: SLA Monitor v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w224_sla_monitor import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w224_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w224_create(client):
    r = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    assert r.status_code == 201
    data = r.json()
    assert "sla_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w224_list(client):
    await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    r = await client.get("/api/sla-monitor")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w224_get_by_id(client):
    r = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    item_id = r.json()["sla_id"]
    r2 = await client.get(f"/api/sla-monitor/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["sla_id"] == item_id

@pytest.mark.asyncio
async def test_w224_get_not_found(client):
    r = await client.get("/api/sla-monitor/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w224_check_breach(client):
    r = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    item_id = r.json()["sla_id"]
    r2 = await client.post(f"/api/sla-monitor/{item_id}/breach", json={})
    assert r2.status_code == 200
    assert r2.json()["sla_id"] == item_id

@pytest.mark.asyncio
async def test_w224_escalate(client):
    r = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    item_id = r.json()["sla_id"]
    r2 = await client.post(f"/api/sla-monitor/{item_id}/escalate", json={})
    assert r2.status_code == 200
    assert r2.json()["sla_id"] == item_id

@pytest.mark.asyncio
async def test_w224_check_breach_not_found(client):
    r = await client.post("/api/sla-monitor/nonexistent-id/breach", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w224_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "sla_monitor"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w224_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "sla_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w224_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/sla-monitor", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w224_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/sla-monitor", json={'task_id': 'test-task_id', 'task_name': 'test-task_name', 'expected_duration_min': 1, 'actual_duration_min': 1, 'deadline': 'test-deadline', 'breach_risk_pct': 1.0, 'breached': True, 'escalation_sent': True, 'escalation_target': 'test-escalation_target', 'variance_min': 1, 'status': 'test-status', 'monitored_at': 'test-monitored_at'})
    assert r1.status_code == 201
    item_id = r1.json()["sla_id"]
    r2 = await client.get("/api/sla-monitor")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/sla-monitor/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["sla_id"] == item_id
