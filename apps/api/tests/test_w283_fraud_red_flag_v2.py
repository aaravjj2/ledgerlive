"""Tests for Wave 283: Fraud Red Flag Engine v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w283_fraud_red_flag_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w283_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w283_create(client):
    r = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert r.status_code == 201
    data = r.json()
    assert "flag_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w283_list(client):
    await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    r = await client.get("/api/fraud-red-flag-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w283_get_by_id(client):
    r = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["flag_id"]
    r2 = await client.get(f"/api/fraud-red-flag-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["flag_id"] == item_id

@pytest.mark.asyncio
async def test_w283_get_not_found(client):
    r = await client.get("/api/fraud-red-flag-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w283_assess_risk(client):
    r = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["flag_id"]
    r2 = await client.post(f"/api/fraud-red-flag-v2/{item_id}/assess", json={})
    assert r2.status_code == 200
    assert r2.json()["flag_id"] == item_id

@pytest.mark.asyncio
async def test_w283_approve_action(client):
    r = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["flag_id"]
    r2 = await client.post(f"/api/fraud-red-flag-v2/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["flag_id"] == item_id

@pytest.mark.asyncio
async def test_w283_link_dossier(client):
    r = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["flag_id"]
    r2 = await client.post(f"/api/fraud-red-flag-v2/{item_id}/dossier", json={})
    assert r2.status_code == 200
    assert r2.json()["flag_id"] == item_id

@pytest.mark.asyncio
async def test_w283_assess_risk_not_found(client):
    r = await client.post("/api/fraud-red-flag-v2/nonexistent-id/assess", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w283_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "fraud_red_flag_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w283_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "flag_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w283_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/fraud-red-flag-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w283_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/fraud-red-flag-v2", json={'detection_type': 'test-detection_type', 'entity_ref': 'test-entity_ref', 'risk_score': 1.0, 'confidence': 1.0, 'red_flag_reason': 'test-red_flag_reason', 'dossier_ref': 'test-dossier_ref', 'approval_required': True, 'approved_by': 'test-approved_by', 'evidence_refs': [], 'similar_entities': [], 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert r1.status_code == 201
    item_id = r1.json()["flag_id"]
    r2 = await client.get("/api/fraud-red-flag-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/fraud-red-flag-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["flag_id"] == item_id
