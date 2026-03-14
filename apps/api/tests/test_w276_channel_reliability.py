"""Tests for Wave 276: Channel Reliability Harness v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w276_channel_reliability import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w276_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w276_create(client):
    r = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "harness_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w276_list(client):
    await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/channel-reliability")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w276_get_by_id(client):
    r = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["harness_id"]
    r2 = await client.get(f"/api/channel-reliability/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["harness_id"] == item_id

@pytest.mark.asyncio
async def test_w276_get_not_found(client):
    r = await client.get("/api/channel-reliability/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w276_inject_failure(client):
    r = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["harness_id"]
    r2 = await client.post(f"/api/channel-reliability/{item_id}/inject", json={})
    assert r2.status_code == 200
    assert r2.json()["harness_id"] == item_id

@pytest.mark.asyncio
async def test_w276_test_recovery(client):
    r = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["harness_id"]
    r2 = await client.post(f"/api/channel-reliability/{item_id}/recover", json={})
    assert r2.status_code == 200
    assert r2.json()["harness_id"] == item_id

@pytest.mark.asyncio
async def test_w276_inject_failure_not_found(client):
    r = await client.post("/api/channel-reliability/nonexistent-id/inject", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w276_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "channel_reliability"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w276_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "harness_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w276_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/channel-reliability", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w276_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/channel-reliability", json={'channel_type': 'test-channel_type', 'failure_type': 'test-failure_type', 'failure_config': {}, 'recovery_strategy': 'test-recovery_strategy', 'recovery_successful': True, 'retry_count': 1, 'max_retries': 1, 'partial_delivery_pct': 1.0, 'timeout_ms': 1, 'deterministic_outcome': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["harness_id"]
    r2 = await client.get("/api/channel-reliability")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/channel-reliability/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["harness_id"] == item_id
