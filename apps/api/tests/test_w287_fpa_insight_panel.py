"""Tests for Wave 287: FP&A Insight Panel v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w287_fpa_insight_panel import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w287_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w287_create(client):
    r = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "insight_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w287_list(client):
    await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    r = await client.get("/api/fpa-insight-panel")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w287_get_by_id(client):
    r = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["insight_id"]
    r2 = await client.get(f"/api/fpa-insight-panel/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["insight_id"] == item_id

@pytest.mark.asyncio
async def test_w287_get_not_found(client):
    r = await client.get("/api/fpa-insight-panel/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w287_analyze_variance(client):
    r = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["insight_id"]
    r2 = await client.post(f"/api/fpa-insight-panel/{item_id}/variance", json={})
    assert r2.status_code == 200
    assert r2.json()["insight_id"] == item_id

@pytest.mark.asyncio
async def test_w287_run_scenario(client):
    r = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["insight_id"]
    r2 = await client.post(f"/api/fpa-insight-panel/{item_id}/scenario", json={})
    assert r2.status_code == 200
    assert r2.json()["insight_id"] == item_id

@pytest.mark.asyncio
async def test_w287_analyze_variance_not_found(client):
    r = await client.post("/api/fpa-insight-panel/nonexistent-id/variance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w287_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "fpa_insight_panel"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w287_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "insight_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w287_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/fpa-insight-panel", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w287_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/fpa-insight-panel", json={'period_ref': 'test-period_ref', 'budget_data': {}, 'forecast_data': {}, 'scenario_deltas': [], 'variance_analysis': {}, 'key_drivers': [], 'telemetry_ref': 'test-telemetry_ref', 'rc_display_config': {}, 'deterministic': True, 'confidence_level': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["insight_id"]
    r2 = await client.get("/api/fpa-insight-panel")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/fpa-insight-panel/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["insight_id"] == item_id
