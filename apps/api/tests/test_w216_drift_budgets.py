"""Tests for Wave 216: Drift Monitoring Budgets Enforced

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w216_drift_budgets import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w216_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w216_create(client):
    r = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "budget_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w216_list(client):
    await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/drift-budgets")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w216_get_by_id(client):
    r = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.get(f"/api/drift-budgets/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w216_get_not_found(client):
    r = await client.get("/api/drift-budgets/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w216_check_regression(client):
    r = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/drift-budgets/{item_id}/regression", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w216_enforce_threshold(client):
    r = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/drift-budgets/{item_id}/enforce", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w216_check_regression_not_found(client):
    r = await client.post("/api/drift-budgets/nonexistent-id/regression", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w216_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "drift_budgets"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w216_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "budget_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w216_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/drift-budgets", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w216_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/drift-budgets", json={'release_tag': 'test-release_tag', 'dataset_hash': 'test-dataset_hash', 'model_hash': 'test-model_hash', 'metrics_snapshot': {}, 'thresholds': {}, 'budget_pass': True, 'regression_detected': True, 'regressed_metrics': [], 'drift_report_hash': 'test-drift_report_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["budget_id"]
    r2 = await client.get("/api/drift-budgets")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/drift-budgets/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["budget_id"] == item_id
