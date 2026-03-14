"""Tests for Wave 52: Forecasting 1.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w52_forecasting import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w52_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w52_create(client):
    r = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "forecast_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w52_list(client):
    await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/forecasts")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w52_get_by_id(client):
    r = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["forecast_id"]
    r2 = await client.get(f"/api/forecasts/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["forecast_id"] == item_id

@pytest.mark.asyncio
async def test_w52_get_not_found(client):
    r = await client.get("/api/forecasts/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w52_evaluate(client):
    r = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["forecast_id"]
    r2 = await client.post(f"/api/forecasts/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["forecast_id"] == item_id

@pytest.mark.asyncio
async def test_w52_detect_drift(client):
    r = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["forecast_id"]
    r2 = await client.post(f"/api/forecasts/{item_id}/drift", json={})
    assert r2.status_code == 200
    assert r2.json()["forecast_id"] == item_id

@pytest.mark.asyncio
async def test_w52_register_model(client):
    r = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["forecast_id"]
    r2 = await client.post(f"/api/forecasts/{item_id}/register", json={})
    assert r2.status_code == 200
    assert r2.json()["forecast_id"] == item_id

@pytest.mark.asyncio
async def test_w52_evaluate_not_found(client):
    r = await client.post("/api/forecasts/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w52_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "forecasting"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w52_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "forecast_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w52_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/forecasts", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w52_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/forecasts", json={'model_type': 'test-model_type', 'model_name': 'test-model_name', 'horizon_periods': 1, 'predictions': [], 'mape': 1.0, 'drift_detected': True, 'baseline_hash': 'test-baseline_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["forecast_id"]
    r2 = await client.get("/api/forecasts")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/forecasts/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["forecast_id"] == item_id
