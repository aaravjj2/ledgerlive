"""Tests for Wave 158: No Drift Meta-Guards

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w158_no_drift_guard import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w158_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w158_create(client):
    r = await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "guard_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w158_list(client):
    await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/no-drift-guards")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w158_get_by_id(client):
    r = await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["guard_id"]
    r2 = await client.get(f"/api/no-drift-guards/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["guard_id"] == item_id

@pytest.mark.asyncio
async def test_w158_get_not_found(client):
    r = await client.get("/api/no-drift-guards/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w158_check_drift(client):
    r = await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["guard_id"]
    r2 = await client.post(f"/api/no-drift-guards/{item_id}/check", json={})
    assert r2.status_code == 200
    assert r2.json()["guard_id"] == item_id

@pytest.mark.asyncio
async def test_w158_check_drift_not_found(client):
    r = await client.post("/api/no-drift-guards/nonexistent-id/check", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w158_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "no_drift_guard"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w158_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "guard_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w158_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/no-drift-guards", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w158_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/no-drift-guards", json={'guard_type': 'test-guard_type', 'baseline_hash': 'test-baseline_hash', 'current_hash': 'test-current_hash', 'drift_detected': True, 'drift_details': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["guard_id"]
    r2 = await client.get("/api/no-drift-guards")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/no-drift-guards/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["guard_id"] == item_id
