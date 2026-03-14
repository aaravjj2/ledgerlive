"""Tests for Wave 6: Reconciliation Engine

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w06_reconciliation import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w06_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w06_create(client):
    r = await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    assert r.status_code == 201
    data = r.json()
    assert "recon_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w06_list(client):
    await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    r = await client.get("/api/reconciliations")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w06_get_by_id(client):
    r = await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    item_id = r.json()["recon_id"]
    r2 = await client.get(f"/api/reconciliations/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["recon_id"] == item_id

@pytest.mark.asyncio
async def test_w06_get_not_found(client):
    r = await client.get("/api/reconciliations/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w06_approve(client):
    r = await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    item_id = r.json()["recon_id"]
    r2 = await client.post(f"/api/reconciliations/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["recon_id"] == item_id

@pytest.mark.asyncio
async def test_w06_reject(client):
    r = await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    item_id = r.json()["recon_id"]
    r2 = await client.post(f"/api/reconciliations/{item_id}/reject", json={})
    assert r2.status_code == 200
    assert r2.json()["recon_id"] == item_id

@pytest.mark.asyncio
async def test_w06_approve_not_found(client):
    r = await client.post("/api/reconciliations/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w06_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "reconciliation"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w06_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/reconciliations", json={'period_id': 'test-period_id', 'source_type': 'test-source_type', 'target_type': 'test-target_type', 'match_score': 1.0, 'status': 'test-status', 'explanation': 'test-explanation', 'matched_at': 'test-matched_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "recon_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w06_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/reconciliations", json={})
    assert r.status_code == 201
