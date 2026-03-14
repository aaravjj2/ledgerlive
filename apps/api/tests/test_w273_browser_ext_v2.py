"""Tests for Wave 273: Browser Extension v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w273_browser_ext_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w273_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w273_create(client):
    r = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "capture_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w273_list(client):
    await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    r = await client.get("/api/browser-ext-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w273_get_by_id(client):
    r = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["capture_id"]
    r2 = await client.get(f"/api/browser-ext-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["capture_id"] == item_id

@pytest.mark.asyncio
async def test_w273_get_not_found(client):
    r = await client.get("/api/browser-ext-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w273_annotate(client):
    r = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["capture_id"]
    r2 = await client.post(f"/api/browser-ext-v2/{item_id}/annotate", json={})
    assert r2.status_code == 200
    assert r2.json()["capture_id"] == item_id

@pytest.mark.asyncio
async def test_w273_submit_capture(client):
    r = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["capture_id"]
    r2 = await client.post(f"/api/browser-ext-v2/{item_id}/submit", json={})
    assert r2.status_code == 200
    assert r2.json()["capture_id"] == item_id

@pytest.mark.asyncio
async def test_w273_annotate_not_found(client):
    r = await client.post("/api/browser-ext-v2/nonexistent-id/annotate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w273_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "browser_ext_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w273_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "capture_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w273_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/browser-ext-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w273_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/browser-ext-v2", json={'url': 'test-url', 'capture_data': {}, 'annotations': [], 'submission_ref': 'test-submission_ref', 'evidence_link': 'test-evidence_link', 'deep_link': 'test-deep_link', 'capture_hash': 'test-capture_hash', 'fixture_id': 'test-fixture_id', 'deterministic': True, 'render_consistent': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["capture_id"]
    r2 = await client.get("/api/browser-ext-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/browser-ext-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["capture_id"] == item_id
