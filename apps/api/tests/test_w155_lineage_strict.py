"""Tests for Wave 155: Lineage Verifier Strict Mode

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w155_lineage_strict import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w155_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w155_create(client):
    r = await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "verifier_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w155_list(client):
    await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/lineage-strict")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w155_get_by_id(client):
    r = await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verifier_id"]
    r2 = await client.get(f"/api/lineage-strict/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["verifier_id"] == item_id

@pytest.mark.asyncio
async def test_w155_get_not_found(client):
    r = await client.get("/api/lineage-strict/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w155_check_ref(client):
    r = await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verifier_id"]
    r2 = await client.post(f"/api/lineage-strict/{item_id}/check", json={})
    assert r2.status_code == 200
    assert r2.json()["verifier_id"] == item_id

@pytest.mark.asyncio
async def test_w155_check_ref_not_found(client):
    r = await client.post("/api/lineage-strict/nonexistent-id/check", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w155_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "lineage_strict"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w155_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "verifier_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w155_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/lineage-strict", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w155_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/lineage-strict", json={'lineage_refs': [], 'all_verified': True, 'unverified_refs': [], 'strict_mode': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["verifier_id"]
    r2 = await client.get("/api/lineage-strict")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/lineage-strict/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["verifier_id"] == item_id
