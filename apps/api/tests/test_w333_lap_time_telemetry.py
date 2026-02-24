"""Tests for Wave 333: Lap Time Telemetry v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w333_lap_time_telemetry import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w333_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w333_create(client):
    r = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    assert r.status_code == 201
    data = r.json()
    assert "lap_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w333_list(client):
    await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    r = await client.get("/api/lap-time-telemetry")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w333_get_by_id(client):
    r = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    item_id = r.json()["lap_id"]
    r2 = await client.get(f"/api/lap-time-telemetry/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["lap_id"] == item_id

@pytest.mark.asyncio
async def test_w333_get_not_found(client):
    r = await client.get("/api/lap-time-telemetry/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w333_bucket_analysis(client):
    r = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    item_id = r.json()["lap_id"]
    r2 = await client.post(f"/api/lap-time-telemetry/{item_id}/bucket", json={})
    assert r2.status_code == 200
    assert r2.json()["lap_id"] == item_id

@pytest.mark.asyncio
async def test_w333_heatmap_data(client):
    r = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    item_id = r.json()["lap_id"]
    r2 = await client.post(f"/api/lap-time-telemetry/{item_id}/heatmap", json={})
    assert r2.status_code == 200
    assert r2.json()["lap_id"] == item_id

@pytest.mark.asyncio
async def test_w333_bucket_analysis_not_found(client):
    r = await client.post("/api/lap-time-telemetry/nonexistent-id/bucket", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w333_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "lap_time_telemetry"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w333_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "lap_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w333_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/lap-time-telemetry", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w333_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/lap-time-telemetry", json={'step_name': 'test-step_name', 'duration_ms': 1, 'bucket': 'test-bucket', 'is_critical_path': True, 'heatmap_color': 'test-heatmap_color', 'sequence_num': 1, 'parent_lap_ref': 'test-parent_lap_ref', 'percentile_rank': 1.0, 'deterministic': True, 'status': 'test-status', 'recorded_at': 'test-recorded_at'})
    assert r1.status_code == 201
    item_id = r1.json()["lap_id"]
    r2 = await client.get("/api/lap-time-telemetry")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/lap-time-telemetry/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["lap_id"] == item_id
