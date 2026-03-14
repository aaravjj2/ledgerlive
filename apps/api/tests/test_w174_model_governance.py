"""Tests for Wave 174: Model Governance Lite

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w174_model_governance import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w174_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w174_create(client):
    r = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "governance_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w174_list(client):
    await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/model-governance")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w174_get_by_id(client):
    r = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["governance_id"]
    r2 = await client.get(f"/api/model-governance/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["governance_id"] == item_id

@pytest.mark.asyncio
async def test_w174_get_not_found(client):
    r = await client.get("/api/model-governance/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w174_compute_drift(client):
    r = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["governance_id"]
    r2 = await client.post(f"/api/model-governance/{item_id}/drift", json={})
    assert r2.status_code == 200
    assert r2.json()["governance_id"] == item_id

@pytest.mark.asyncio
async def test_w174_verify_stability(client):
    r = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["governance_id"]
    r2 = await client.post(f"/api/model-governance/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["governance_id"] == item_id

@pytest.mark.asyncio
async def test_w174_compute_drift_not_found(client):
    r = await client.post("/api/model-governance/nonexistent-id/drift", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w174_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "model_governance"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w174_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "governance_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w174_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/model-governance", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w174_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/model-governance", json={'model_id': 'test-model_id', 'dataset_id': 'test-dataset_id', 'drift_detected': True, 'drift_score': 1.0, 'drift_report_hash': 'test-drift_report_hash', 'eval_metrics': {}, 'snapshot_stable': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["governance_id"]
    r2 = await client.get("/api/model-governance")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/model-governance/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["governance_id"] == item_id
