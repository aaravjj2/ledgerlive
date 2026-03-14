"""Tests for Wave 75: Triage Queue 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w075_triage_queue_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w075_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w075_create(client):
    r = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    assert r.status_code == 201
    data = r.json()
    assert "triage_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w075_list(client):
    await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    r = await client.get("/api/triage-queue-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w075_get_by_id(client):
    r = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["triage_id"]
    r2 = await client.get(f"/api/triage-queue-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["triage_id"] == item_id

@pytest.mark.asyncio
async def test_w075_get_not_found(client):
    r = await client.get("/api/triage-queue-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w075_escalate(client):
    r = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["triage_id"]
    r2 = await client.post(f"/api/triage-queue-v2/{item_id}/escalate", json={})
    assert r2.status_code == 200
    assert r2.json()["triage_id"] == item_id

@pytest.mark.asyncio
async def test_w075_resolve(client):
    r = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["triage_id"]
    r2 = await client.post(f"/api/triage-queue-v2/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["triage_id"] == item_id

@pytest.mark.asyncio
async def test_w075_escalate_not_found(client):
    r = await client.post("/api/triage-queue-v2/nonexistent-id/escalate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w075_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "triage_queue_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w075_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "triage_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w075_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/triage-queue-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w075_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/triage-queue-v2", json={'exception_id': 'test-exception_id', 'priority': 1, 'assigned_to': 'test-assigned_to', 'escalation_level': 1, 'escalation_policy': 'test-escalation_policy', 'sla_deadline': 'test-sla_deadline', 'status': 'test-status', 'triaged_at': 'test-triaged_at', 'resolved_at': 'test-resolved_at'})
    assert r1.status_code == 201
    item_id = r1.json()["triage_id"]
    r2 = await client.get("/api/triage-queue-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/triage-queue-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["triage_id"] == item_id
