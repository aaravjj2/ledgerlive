"""Tests for Wave 173: ML Inference Hook v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w173_ml_inference import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w173_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w173_create(client):
    r = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    assert r.status_code == 201
    data = r.json()
    assert "inference_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w173_list(client):
    await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    r = await client.get("/api/ml-inference")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w173_get_by_id(client):
    r = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    item_id = r.json()["inference_id"]
    r2 = await client.get(f"/api/ml-inference/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["inference_id"] == item_id

@pytest.mark.asyncio
async def test_w173_get_not_found(client):
    r = await client.get("/api/ml-inference/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w173_explain_decision(client):
    r = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    item_id = r.json()["inference_id"]
    r2 = await client.post(f"/api/ml-inference/{item_id}/explain", json={})
    assert r2.status_code == 200
    assert r2.json()["inference_id"] == item_id

@pytest.mark.asyncio
async def test_w173_fallback_check(client):
    r = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    item_id = r.json()["inference_id"]
    r2 = await client.post(f"/api/ml-inference/{item_id}/fallback", json={})
    assert r2.status_code == 200
    assert r2.json()["inference_id"] == item_id

@pytest.mark.asyncio
async def test_w173_explain_decision_not_found(client):
    r = await client.post("/api/ml-inference/nonexistent-id/explain", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w173_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ml_inference"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w173_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "inference_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w173_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ml-inference", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w173_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/ml-inference", json={'model_id': 'test-model_id', 'input_hash': 'test-input_hash', 'confidence': 1.0, 'routing_decision': 'test-routing_decision', 'explanation': 'test-explanation', 'evidence_pointers': [], 'verifier_pass': True, 'fallback_used': True, 'status': 'test-status', 'inferred_at': 'test-inferred_at'})
    assert r1.status_code == 201
    item_id = r1.json()["inference_id"]
    r2 = await client.get("/api/ml-inference")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ml-inference/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["inference_id"] == item_id
