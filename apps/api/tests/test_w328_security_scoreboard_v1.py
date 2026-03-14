"""Tests for Wave 328: Security Scoreboard v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w328_security_scoreboard_v1 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w328_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w328_create(client):
    r = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    assert r.status_code == 201
    data = r.json()
    assert "score_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w328_list(client):
    await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    r = await client.get("/api/security-scoreboard-v1")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w328_get_by_id(client):
    r = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    item_id = r.json()["score_id"]
    r2 = await client.get(f"/api/security-scoreboard-v1/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["score_id"] == item_id

@pytest.mark.asyncio
async def test_w328_get_not_found(client):
    r = await client.get("/api/security-scoreboard-v1/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w328_recalculate(client):
    r = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    item_id = r.json()["score_id"]
    r2 = await client.post(f"/api/security-scoreboard-v1/{item_id}/recalculate", json={})
    assert r2.status_code == 200
    assert r2.json()["score_id"] == item_id

@pytest.mark.asyncio
async def test_w328_export_metrics(client):
    r = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    item_id = r.json()["score_id"]
    r2 = await client.post(f"/api/security-scoreboard-v1/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["score_id"] == item_id

@pytest.mark.asyncio
async def test_w328_recalculate_not_found(client):
    r = await client.post("/api/security-scoreboard-v1/nonexistent-id/recalculate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w328_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "security_scoreboard_v1"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w328_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "score_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w328_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/security-scoreboard-v1", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w328_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/security-scoreboard-v1", json={'period_ref': 'test-period_ref', 'blocked_count': 1, 'block_reasons': [], 'remediation_attempted': 1, 'remediation_succeeded': 1, 'success_rate': 1.0, 'top_threats': [], 'score': 1.0, 'deterministic': True, 'status': 'test-status', 'scored_at': 'test-scored_at'})
    assert r1.status_code == 201
    item_id = r1.json()["score_id"]
    r2 = await client.get("/api/security-scoreboard-v1")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/security-scoreboard-v1/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["score_id"] == item_id
