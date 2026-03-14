"""Tests for Wave 334: Productivity ROI Estimator v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w334_productivity_roi import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w334_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w334_create(client):
    r = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "roi_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w334_list(client):
    await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    r = await client.get("/api/productivity-roi")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w334_get_by_id(client):
    r = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    item_id = r.json()["roi_id"]
    r2 = await client.get(f"/api/productivity-roi/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["roi_id"] == item_id

@pytest.mark.asyncio
async def test_w334_get_not_found(client):
    r = await client.get("/api/productivity-roi/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w334_recalculate(client):
    r = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    item_id = r.json()["roi_id"]
    r2 = await client.post(f"/api/productivity-roi/{item_id}/recalculate", json={})
    assert r2.status_code == 200
    assert r2.json()["roi_id"] == item_id

@pytest.mark.asyncio
async def test_w334_export_report(client):
    r = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    item_id = r.json()["roi_id"]
    r2 = await client.post(f"/api/productivity-roi/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["roi_id"] == item_id

@pytest.mark.asyncio
async def test_w334_recalculate_not_found(client):
    r = await client.post("/api/productivity-roi/nonexistent-id/recalculate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w334_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "productivity_roi"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w334_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "roi_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w334_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/productivity-roi", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w334_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/productivity-roi", json={'period_ref': 'test-period_ref', 'time_saved_hours': 1.0, 'exceptions_prevented': 1, 'sla_compliance_pct': 1.0, 'cost_savings': 1.0, 'roi_multiplier': 1.0, 'calculation_method': 'test-calculation_method', 'baseline_ref': 'test-baseline_ref', 'deterministic': True, 'status': 'test-status', 'calculated_at': 'test-calculated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["roi_id"]
    r2 = await client.get("/api/productivity-roi")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/productivity-roi/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["roi_id"] == item_id
