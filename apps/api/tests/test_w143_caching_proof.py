"""Tests for Wave 143: Caching with Output Proofs

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w143_caching_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w143_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w143_create(client):
    r = await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "cache_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w143_list(client):
    await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/caching-proofs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w143_get_by_id(client):
    r = await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["cache_id"]
    r2 = await client.get(f"/api/caching-proofs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["cache_id"] == item_id

@pytest.mark.asyncio
async def test_w143_get_not_found(client):
    r = await client.get("/api/caching-proofs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w143_verify_output(client):
    r = await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["cache_id"]
    r2 = await client.post(f"/api/caching-proofs/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["cache_id"] == item_id

@pytest.mark.asyncio
async def test_w143_verify_output_not_found(client):
    r = await client.post("/api/caching-proofs/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w143_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "caching_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w143_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "cache_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w143_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/caching-proofs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w143_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/caching-proofs", json={'cache_key': 'test-cache_key', 'uncached_hash': 'test-uncached_hash', 'cached_hash': 'test-cached_hash', 'outputs_match': True, 'hit_rate_pct': 1.0, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["cache_id"]
    r2 = await client.get("/api/caching-proofs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/caching-proofs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["cache_id"] == item_id
