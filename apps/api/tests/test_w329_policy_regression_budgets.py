"""Tests for Wave 329: Policy Regression Budgets v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w329_policy_regression_budgets import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w329_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w329_create(client):
    r = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "budget_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w329_list(client):
    await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/policy-regression-budgets")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w329_get_by_id(client):
    r = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.get(f"/api/policy-regression-budgets/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w329_get_not_found(client):
    r = await client.get("/api/policy-regression-budgets/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w329_evaluate_regression(client):
    r = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/policy-regression-budgets/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w329_reset_baseline(client):
    r = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/policy-regression-budgets/{item_id}/reset", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w329_evaluate_regression_not_found(client):
    r = await client.post("/api/policy-regression-budgets/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w329_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "policy_regression_budgets"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w329_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "budget_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w329_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/policy-regression-budgets", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w329_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/policy-regression-budgets", json={'policy_ref': 'test-policy_ref', 'baseline_coverage': 1.0, 'current_coverage': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'regression_threshold': 1.0, 'explainability_score': 1.0, 'detection_score': 1.0, 'budget_exceeded': True, 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["budget_id"]
    r2 = await client.get("/api/policy-regression-budgets")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/policy-regression-budgets/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["budget_id"] == item_id
