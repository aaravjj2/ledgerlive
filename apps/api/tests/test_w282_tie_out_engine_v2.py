"""Tests for Wave 282: Tie-Out Engine v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w282_tie_out_engine_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w282_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w282_create(client):
    r = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "tie_out_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w282_list(client):
    await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/tie-out-engine-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w282_get_by_id(client):
    r = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["tie_out_id"]
    r2 = await client.get(f"/api/tie-out-engine-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["tie_out_id"] == item_id

@pytest.mark.asyncio
async def test_w282_get_not_found(client):
    r = await client.get("/api/tie-out-engine-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w282_evaluate_variance(client):
    r = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["tie_out_id"]
    r2 = await client.post(f"/api/tie-out-engine-v2/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["tie_out_id"] == item_id

@pytest.mark.asyncio
async def test_w282_create_incident_from_variance(client):
    r = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["tie_out_id"]
    r2 = await client.post(f"/api/tie-out-engine-v2/{item_id}/incident", json={})
    assert r2.status_code == 200
    assert r2.json()["tie_out_id"] == item_id

@pytest.mark.asyncio
async def test_w282_evaluate_variance_not_found(client):
    r = await client.post("/api/tie-out-engine-v2/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w282_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tie_out_engine_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w282_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "tie_out_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w282_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/tie-out-engine-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w282_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/tie-out-engine-v2", json={'rule_name': 'test-rule_name', 'source_value': 1.0, 'target_value': 1.0, 'variance': 1.0, 'threshold': 1.0, 'within_threshold': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'evidence_refs': [], 'rule_config': {}, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["tie_out_id"]
    r2 = await client.get("/api/tie-out-engine-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/tie-out-engine-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["tie_out_id"] == item_id
