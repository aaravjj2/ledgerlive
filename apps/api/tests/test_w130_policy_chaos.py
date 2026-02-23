"""Tests for Wave 130: Policy Chaos Tests

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w130_policy_chaos import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w130_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w130_create(client):
    r = await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "chaos_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w130_list(client):
    await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/policy-chaos")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w130_get_by_id(client):
    r = await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["chaos_id"]
    r2 = await client.get(f"/api/policy-chaos/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["chaos_id"] == item_id

@pytest.mark.asyncio
async def test_w130_get_not_found(client):
    r = await client.get("/api/policy-chaos/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w130_verify_chaos(client):
    r = await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["chaos_id"]
    r2 = await client.post(f"/api/policy-chaos/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["chaos_id"] == item_id

@pytest.mark.asyncio
async def test_w130_verify_chaos_not_found(client):
    r = await client.post("/api/policy-chaos/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w130_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "policy_chaos"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w130_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "chaos_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w130_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/policy-chaos", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w130_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/policy-chaos", json={'scenario': 'test-scenario', 'policy_enforced': True, 'outcome_deterministic': True, 'deny_reason_stable': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["chaos_id"]
    r2 = await client.get("/api/policy-chaos")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/policy-chaos/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["chaos_id"] == item_id
