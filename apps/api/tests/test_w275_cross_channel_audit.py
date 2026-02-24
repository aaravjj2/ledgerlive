"""Tests for Wave 275: Cross-Channel Audit v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w275_cross_channel_audit import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w275_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w275_create(client):
    r = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    assert r.status_code == 201
    data = r.json()
    assert "audit_entry_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w275_list(client):
    await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    r = await client.get("/api/cross-channel-audit")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w275_get_by_id(client):
    r = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    item_id = r.json()["audit_entry_id"]
    r2 = await client.get(f"/api/cross-channel-audit/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["audit_entry_id"] == item_id

@pytest.mark.asyncio
async def test_w275_get_not_found(client):
    r = await client.get("/api/cross-channel-audit/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w275_link_trace(client):
    r = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    item_id = r.json()["audit_entry_id"]
    r2 = await client.post(f"/api/cross-channel-audit/{item_id}/trace", json={})
    assert r2.status_code == 200
    assert r2.json()["audit_entry_id"] == item_id

@pytest.mark.asyncio
async def test_w275_update_dossier(client):
    r = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    item_id = r.json()["audit_entry_id"]
    r2 = await client.post(f"/api/cross-channel-audit/{item_id}/dossier", json={})
    assert r2.status_code == 200
    assert r2.json()["audit_entry_id"] == item_id

@pytest.mark.asyncio
async def test_w275_link_trace_not_found(client):
    r = await client.post("/api/cross-channel-audit/nonexistent-id/trace", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w275_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "cross_channel_audit"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w275_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "audit_entry_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w275_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/cross-channel-audit", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w275_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/cross-channel-audit", json={'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'action_ref': 'test-action_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'dossier_ref': 'test-dossier_ref', 'user_id': 'test-user_id', 'timestamp': 'test-timestamp', 'evidence_refs': [], 'context_data': {}, 'ordering_key': 1, 'deterministic': True, 'status': 'test-status'})
    assert r1.status_code == 201
    item_id = r1.json()["audit_entry_id"]
    r2 = await client.get("/api/cross-channel-audit")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/cross-channel-audit/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["audit_entry_id"] == item_id
