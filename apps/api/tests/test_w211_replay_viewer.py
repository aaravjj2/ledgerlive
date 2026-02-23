"""Tests for Wave 211: Replay Viewer UI v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w211_replay_viewer import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w211_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w211_create(client):
    r = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    assert r.status_code == 201
    data = r.json()
    assert "viewer_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w211_list(client):
    await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    r = await client.get("/api/replay-viewer")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w211_get_by_id(client):
    r = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.get(f"/api/replay-viewer/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w211_get_not_found(client):
    r = await client.get("/api/replay-viewer/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w211_step_forward(client):
    r = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.post(f"/api/replay-viewer/{item_id}/step", json={})
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w211_open_dossier(client):
    r = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.post(f"/api/replay-viewer/{item_id}/dossier", json={})
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w211_highlight_evidence(client):
    r = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    item_id = r.json()["viewer_id"]
    r2 = await client.post(f"/api/replay-viewer/{item_id}/highlight", json={})
    assert r2.status_code == 200
    assert r2.json()["viewer_id"] == item_id

@pytest.mark.asyncio
async def test_w211_step_forward_not_found(client):
    r = await client.post("/api/replay-viewer/nonexistent-id/step", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w211_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "replay_viewer"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w211_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "viewer_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w211_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/replay-viewer", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w211_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/replay-viewer", json={'replay_id': 'test-replay_id', 'timeline_steps': [], 'tool_trace_rows': [], 'dossier_links': [], 'evidence_spans': [], 'current_step_index': 1, 'page_testid': 'test-page_testid', 'highlight_active': True, 'status': 'test-status', 'opened_at': 'test-opened_at'})
    assert r1.status_code == 201
    item_id = r1.json()["viewer_id"]
    r2 = await client.get("/api/replay-viewer")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/replay-viewer/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["viewer_id"] == item_id
