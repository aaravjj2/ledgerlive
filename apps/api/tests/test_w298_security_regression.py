"""Tests for Wave 298: Security Regression Budgets v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w298_security_regression import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w298_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w298_create(client):
    r = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "regression_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w298_list(client):
    await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/security-regression")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w298_get_by_id(client):
    r = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["regression_id"]
    r2 = await client.get(f"/api/security-regression/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["regression_id"] == item_id

@pytest.mark.asyncio
async def test_w298_get_not_found(client):
    r = await client.get("/api/security-regression/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w298_measure_coverage(client):
    r = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["regression_id"]
    r2 = await client.post(f"/api/security-regression/{item_id}/coverage", json={})
    assert r2.status_code == 200
    assert r2.json()["regression_id"] == item_id

@pytest.mark.asyncio
async def test_w298_measure_explainability(client):
    r = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["regression_id"]
    r2 = await client.post(f"/api/security-regression/{item_id}/explainability", json={})
    assert r2.status_code == 200
    assert r2.json()["regression_id"] == item_id

@pytest.mark.asyncio
async def test_w298_measure_coverage_not_found(client):
    r = await client.post("/api/security-regression/nonexistent-id/coverage", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w298_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "security_regression"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w298_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "regression_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w298_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/security-regression", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w298_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/security-regression", json={'baseline_coverage_pct': 1.0, 'current_coverage_pct': 1.0, 'coverage_delta': 1.0, 'regressed': True, 'deny_explainability_pct': 1.0, 'baseline_explainability_pct': 1.0, 'explainability_regressed': True, 'budget_threshold': 1.0, 'within_budget': True, 'regression_hash': 'test-regression_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["regression_id"]
    r2 = await client.get("/api/security-regression")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/security-regression/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["regression_id"] == item_id
