"""Tests for Wave 261: Replay Viewer v3

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w261_replay_viewer_v3 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w261_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w261_create(client):
    r = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    assert r.status_code == 201
    data = r.json()
    assert "viewer_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w261_list(client):
    await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    r = await client.get("/api/replay-viewer-v3")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w261_get_by_id(client):
    r = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.get(f"/api/replay-viewer-v3/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w261_get_not_found(client):
    r = await client.get("/api/replay-viewer-v3/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w261_compute_diff(client):
    r = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.post(f"/api/replay-viewer-v3/{item_id}/diff", json={})
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w261_jump_to_evidence(client):
    r = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.post(f"/api/replay-viewer-v3/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w261_compute_diff_not_found(client):
    r = await client.post("/api/replay-viewer-v3/nonexistent-id/diff", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w261_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "replay_viewer_v3"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w261_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "viewer_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w261_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/replay-viewer-v3", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w261_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/replay-viewer-v3", json={'original_ref': 'test-original_ref', 'replay_ref': 'test-replay_ref', 'diff_entries': [], 'diff_summary': {}, 'evidence_links': [], 'policy_event_links': [], 'match_pct': 1.0, 'divergence_points': [], 'render_hash': 'test-render_hash', 'navigation_index': {}, 'status': 'test-status', 'compared_at': 'test-compared_at'})
    assert r1.status_code == 201
    item_id = r1.json()["viewer_id"]
    r2 = await client.get("/api/replay-viewer-v3")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/replay-viewer-v3/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["viewer_id"] == item_id
