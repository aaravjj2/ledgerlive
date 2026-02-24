"""Tests for Wave 251: Policy Events v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w251_policy_events import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w251_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w251_create(client):
    r = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert r.status_code == 201
    data = r.json()
    assert "event_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w251_list(client):
    await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    r = await client.get("/api/policy-events")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w251_get_by_id(client):
    r = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["event_id"]
    r2 = await client.get(f"/api/policy-events/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["event_id"] == item_id

@pytest.mark.asyncio
async def test_w251_get_not_found(client):
    r = await client.get("/api/policy-events/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w251_classify_event(client):
    r = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["event_id"]
    r2 = await client.post(f"/api/policy-events/{item_id}/classify", json={})
    assert r2.status_code == 200
    assert r2.json()["event_id"] == item_id

@pytest.mark.asyncio
async def test_w251_link_evidence(client):
    r = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["event_id"]
    r2 = await client.post(f"/api/policy-events/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["event_id"] == item_id

@pytest.mark.asyncio
async def test_w251_classify_event_not_found(client):
    r = await client.post("/api/policy-events/nonexistent-id/classify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w251_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "policy_events"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w251_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "event_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w251_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/policy-events", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w251_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/policy-events", json={'event_type': 'test-event_type', 'policy_ref': 'test-policy_ref', 'violation_type': 'test-violation_type', 'severity': 'test-severity', 'classification': 'test-classification', 'evidence': {}, 'deny_reason': 'test-deny_reason', 'source_context': {}, 'affected_entities': [], 'remediation_hint': 'test-remediation_hint', 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert r1.status_code == 201
    item_id = r1.json()["event_id"]
    r2 = await client.get("/api/policy-events")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/policy-events/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["event_id"] == item_id
