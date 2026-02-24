"""Tests for Wave 232: Live Scoreboard v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w232_live_scoreboard import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w232_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w232_create(client):
    r = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    assert r.status_code == 201
    data = r.json()
    assert "score_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w232_list(client):
    await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    r = await client.get("/api/live-scoreboard")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w232_get_by_id(client):
    r = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    item_id = r.json()["score_id"]
    r2 = await client.get(f"/api/live-scoreboard/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["score_id"] == item_id

@pytest.mark.asyncio
async def test_w232_get_not_found(client):
    r = await client.get("/api/live-scoreboard/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w232_refresh_score(client):
    r = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    item_id = r.json()["score_id"]
    r2 = await client.post(f"/api/live-scoreboard/{item_id}/refresh", json={})
    assert r2.status_code == 200
    assert r2.json()["score_id"] == item_id

@pytest.mark.asyncio
async def test_w232_rank_teams(client):
    r = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    item_id = r.json()["score_id"]
    r2 = await client.post(f"/api/live-scoreboard/{item_id}/rank", json={})
    assert r2.status_code == 200
    assert r2.json()["score_id"] == item_id

@pytest.mark.asyncio
async def test_w232_refresh_score_not_found(client):
    r = await client.post("/api/live-scoreboard/nonexistent-id/refresh", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w232_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "live_scoreboard"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w232_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "score_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w232_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/live-scoreboard", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w232_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/live-scoreboard", json={'period_id': 'test-period_id', 'team_scores': {}, 'sla_adherence_pct': 1.0, 'blocker_count': 1, 'checkpoints_passed': 1, 'checkpoints_total': 1, 'overall_health': 'test-overall_health', 'trend_indicator': 'test-trend_indicator', 'last_refresh': 'test-last_refresh', 'refresh_interval_s': 1, 'status': 'test-status'})
    assert r1.status_code == 201
    item_id = r1.json()["score_id"]
    r2 = await client.get("/api/live-scoreboard")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/live-scoreboard/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["score_id"] == item_id
