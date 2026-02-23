"""Tests for Wave 186: Gradient Inference Adapter v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w186_gradient_inference import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w186_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w186_create(client):
    r = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "adapter_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w186_list(client):
    await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/gradient-inference")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w186_get_by_id(client):
    r = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.get(f"/api/gradient-inference/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w186_get_not_found(client):
    r = await client.get("/api/gradient-inference/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w186_validate_adapter(client):
    r = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.post(f"/api/gradient-inference/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w186_run_inference(client):
    r = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.post(f"/api/gradient-inference/{item_id}/infer", json={})
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w186_check_fallback(client):
    r = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.post(f"/api/gradient-inference/{item_id}/fallback", json={})
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w186_validate_adapter_not_found(client):
    r = await client.post("/api/gradient-inference/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w186_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "gradient_inference"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w186_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "adapter_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w186_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/gradient-inference", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w186_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/gradient-inference", json={'adapter_name': 'test-adapter_name', 'enabled': True, 'inference_endpoint': 'test-inference_endpoint', 'fallback_mode': True, 'local_artifact_ref': 'test-local_artifact_ref', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'fallback_used': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["adapter_id"]
    r2 = await client.get("/api/gradient-inference")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/gradient-inference/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["adapter_id"] == item_id
