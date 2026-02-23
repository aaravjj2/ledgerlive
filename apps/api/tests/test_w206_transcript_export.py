"""Tests for Wave 206: Transcript Tool Trace Exporter v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w206_transcript_export import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w206_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w206_create(client):
    r = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r.status_code == 201
    data = r.json()
    assert "export_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w206_list(client):
    await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    r = await client.get("/api/transcript-export")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w206_get_by_id(client):
    r = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.get(f"/api/transcript-export/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w206_get_not_found(client):
    r = await client.get("/api/transcript-export/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w206_verify_checksums(client):
    r = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.post(f"/api/transcript-export/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w206_download_pack(client):
    r = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.post(f"/api/transcript-export/{item_id}/download", json={})
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w206_verify_checksums_not_found(client):
    r = await client.post("/api/transcript-export/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w206_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "transcript_export"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w206_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "export_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w206_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/transcript-export", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w206_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/transcript-export", json={'session_id': 'test-session_id', 'transcript_lines': 1, 'tool_trace_lines': 1, 'verifier_results_count': 1, 'checksums': {}, 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'ordering_stable': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r1.status_code == 201
    item_id = r1.json()["export_id"]
    r2 = await client.get("/api/transcript-export")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/transcript-export/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["export_id"] == item_id
