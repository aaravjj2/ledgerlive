"""Tests for Wave 215: Model Impact Dashboard v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w215_model_impact import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w215_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w215_create(client):
    r = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "impact_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w215_list(client):
    await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    r = await client.get("/api/model-impact")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w215_get_by_id(client):
    r = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.get(f"/api/model-impact/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w215_get_not_found(client):
    r = await client.get("/api/model-impact/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w215_compare_baseline(client):
    r = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.post(f"/api/model-impact/{item_id}/compare", json={})
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w215_verify_metrics(client):
    r = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["impact_id"]
    r2 = await client.post(f"/api/model-impact/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["impact_id"] == item_id

@pytest.mark.asyncio
async def test_w215_compare_baseline_not_found(client):
    r = await client.post("/api/model-impact/nonexistent-id/compare", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w215_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "model_impact"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w215_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "impact_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w215_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/model-impact", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w215_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/model-impact", json={'model_id': 'test-model_id', 'eval_run_id': 'test-eval_run_id', 'review_queue_baseline': 1, 'review_queue_with_model': 1, 'volume_reduction_pct': 1.0, 'false_match_baseline': 1, 'false_match_with_model': 1, 'false_match_reduction_pct': 1.0, 'calibration_error': 1.0, 'improvement_pct': 1.0, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["impact_id"]
    r2 = await client.get("/api/model-impact")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/model-impact/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["impact_id"] == item_id
