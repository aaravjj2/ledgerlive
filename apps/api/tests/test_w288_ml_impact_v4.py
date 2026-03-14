"""Tests for Wave 288: ML Impact v4

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w288_ml_impact_v4 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w288_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w288_create(client):
    r = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "impact_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w288_list(client):
    await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/ml-impact-v4")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w288_get_by_id(client):
    r = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.get(f"/api/ml-impact-v4/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w288_get_not_found(client):
    r = await client.get("/api/ml-impact-v4/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w288_compare_models(client):
    r = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.post(f"/api/ml-impact-v4/{item_id}/compare", json={})
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w288_detect_drift(client):
    r = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.post(f"/api/ml-impact-v4/{item_id}/drift", json={})
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w288_create_drift_incident(client):
    r = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.post(f"/api/ml-impact-v4/{item_id}/incident", json={})
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w288_compare_models_not_found(client):
    r = await client.post("/api/ml-impact-v4/nonexistent-id/compare", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w288_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ml_impact_v4"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w288_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "impact_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w288_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ml-impact-v4", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w288_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/ml-impact-v4", json={'model_ref': 'test-model_ref', 'baseline_metrics': {}, 'model_metrics': {}, 'improvement_pct': 1.0, 'drift_detected': True, 'drift_magnitude': 1.0, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'budget_within': True, 'evaluation_hash': 'test-evaluation_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["impact_id"]
    r2 = await client.get("/api/ml-impact-v4")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ml-impact-v4/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["impact_id"] == item_id
