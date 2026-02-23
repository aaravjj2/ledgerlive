"""Tests for Wave 185: Gradient Training Spec v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w185_gradient_training import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w185_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w185_create(client):
    r = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "spec_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w185_list(client):
    await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/gradient-training")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w185_get_by_id(client):
    r = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["spec_id"]
    r2 = await client.get(f"/api/gradient-training/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["spec_id"] == item_id

@pytest.mark.asyncio
async def test_w185_get_not_found(client):
    r = await client.get("/api/gradient-training/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w185_validate_spec(client):
    r = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["spec_id"]
    r2 = await client.post(f"/api/gradient-training/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["spec_id"] == item_id

@pytest.mark.asyncio
async def test_w185_render_plan(client):
    r = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["spec_id"]
    r2 = await client.post(f"/api/gradient-training/{item_id}/render", json={})
    assert r2.status_code == 200
    assert r2.json()["spec_id"] == item_id

@pytest.mark.asyncio
async def test_w185_validate_spec_not_found(client):
    r = await client.post("/api/gradient-training/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w185_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "gradient_training"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w185_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "spec_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w185_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/gradient-training", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w185_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/gradient-training", json={'spec_name': 'test-spec_name', 'spec_type': 'test-spec_type', 'training_config': {}, 'inference_config': {}, 'resource_requirements': {}, 'plan_output': {}, 'plan_hash': 'test-plan_hash', 'validation_errors': [], 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["spec_id"]
    r2 = await client.get("/api/gradient-training")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/gradient-training/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["spec_id"] == item_id
