"""Tests for Wave 172: ML Baseline Models v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w172_ml_baseline import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w172_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w172_create(client):
    r = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    assert r.status_code == 201
    data = r.json()
    assert "model_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w172_list(client):
    await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    r = await client.get("/api/ml-baseline")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w172_get_by_id(client):
    r = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    item_id = r.json()["model_id"]
    r2 = await client.get(f"/api/ml-baseline/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["model_id"] == item_id

@pytest.mark.asyncio
async def test_w172_get_not_found(client):
    r = await client.get("/api/ml-baseline/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w172_evaluate_model(client):
    r = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    item_id = r.json()["model_id"]
    r2 = await client.post(f"/api/ml-baseline/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["model_id"] == item_id

@pytest.mark.asyncio
async def test_w172_register_model(client):
    r = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    item_id = r.json()["model_id"]
    r2 = await client.post(f"/api/ml-baseline/{item_id}/register", json={})
    assert r2.status_code == 200
    assert r2.json()["model_id"] == item_id

@pytest.mark.asyncio
async def test_w172_evaluate_model_not_found(client):
    r = await client.post("/api/ml-baseline/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w172_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ml_baseline"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w172_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "model_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w172_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ml-baseline", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w172_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/ml-baseline", json={'model_name': 'test-model_name', 'model_type': 'test-model_type', 'dataset_id': 'test-dataset_id', 'seed': 1, 'artifact_hash': 'test-artifact_hash', 'calibration_score': 1.0, 'match_accuracy': 1.0, 'metadata': {}, 'status': 'test-status', 'trained_at': 'test-trained_at'})
    assert r1.status_code == 201
    item_id = r1.json()["model_id"]
    r2 = await client.get("/api/ml-baseline")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ml-baseline/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["model_id"] == item_id
