"""Tests for Wave 131: Seeded Chaos Matrix

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w131_chaos_matrix import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w131_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w131_create(client):
    r = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "test_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w131_list(client):
    await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/chaos-matrix")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w131_get_by_id(client):
    r = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["test_id"]
    r2 = await client.get(f"/api/chaos-matrix/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w131_get_not_found(client):
    r = await client.get("/api/chaos-matrix/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w131_verify_determinism(client):
    r = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["test_id"]
    r2 = await client.post(f"/api/chaos-matrix/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w131_inject_failure(client):
    r = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["test_id"]
    r2 = await client.post(f"/api/chaos-matrix/{item_id}/inject", json={})
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w131_verify_determinism_not_found(client):
    r = await client.post("/api/chaos-matrix/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w131_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "chaos_matrix"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w131_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "test_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w131_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/chaos-matrix", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w131_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/chaos-matrix", json={'scenario': 'test-scenario', 'seed': 1, 'failure_type': 'test-failure_type', 'injection_point': 'test-injection_point', 'outcome': 'test-outcome', 'deterministic': True, 'recovery_time_ms': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["test_id"]
    r2 = await client.get("/api/chaos-matrix")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/chaos-matrix/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["test_id"] == item_id
