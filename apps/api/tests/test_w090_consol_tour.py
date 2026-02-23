"""Tests for Wave 90: Consolidation Tour

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w090_consol_tour import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w090_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w090_create(client):
    r = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "tour_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w090_list(client):
    await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/consol-tours")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w090_get_by_id(client):
    r = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.get(f"/api/consol-tours/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w090_get_not_found(client):
    r = await client.get("/api/consol-tours/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w090_run_tour(client):
    r = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.post(f"/api/consol-tours/{item_id}/run", json={})
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w090_verify_determinism(client):
    r = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["tour_id"]
    r2 = await client.post(f"/api/consol-tours/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["tour_id"] == item_id

@pytest.mark.asyncio
async def test_w090_run_tour_not_found(client):
    r = await client.post("/api/consol-tours/nonexistent-id/run", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w090_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "consol_tour"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w090_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "tour_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w090_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/consol-tours", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w090_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/consol-tours", json={'tour_name': 'test-tour_name', 'scenarios': [], 'checkpoints': [], 'duration_s': 1.0, 'determinism_pass': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["tour_id"]
    r2 = await client.get("/api/consol-tours")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/consol-tours/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["tour_id"] == item_id
