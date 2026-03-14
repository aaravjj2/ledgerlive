"""Tests for Wave 69: Tour Spec Manager

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w069_tour_spec import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w069_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w069_create(client):
    r = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "tour_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w069_list(client):
    await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/tour-specs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w069_get_by_id(client):
    r = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.get(f"/api/tour-specs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w069_get_not_found(client):
    r = await client.get("/api/tour-specs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w069_add_checkpoint(client):
    r = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.post(f"/api/tour-specs/{item_id}/checkpoint", json={})
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w069_run_tour(client):
    r = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.post(f"/api/tour-specs/{item_id}/run", json={})
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w069_verify_tour(client):
    r = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.post(f"/api/tour-specs/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w069_add_checkpoint_not_found(client):
    r = await client.post("/api/tour-specs/nonexistent-id/checkpoint", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w069_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tour_spec"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w069_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "tour_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w069_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/tour-specs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w069_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/tour-specs", json={'tour_name': 'test-tour_name', 'checkpoints': [], 'total_duration_s': 1.0, 'checkpoint_count': 1, 'status': 'test-status', 'recording_path': 'test-recording_path', 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["tour_id"]
    r2 = await client.get("/api/tour-specs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/tour-specs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["tour_id"] == item_id
