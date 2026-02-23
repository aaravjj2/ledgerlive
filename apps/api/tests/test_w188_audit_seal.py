"""Tests for Wave 188: Live-Mode Audit Sealing v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w188_audit_seal import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w188_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w188_create(client):
    r = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "seal_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w188_list(client):
    await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    r = await client.get("/api/audit-seal")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w188_get_by_id(client):
    r = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    item_id = r.json()["seal_id"]
    r2 = await client.get(f"/api/audit-seal/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["seal_id"] == item_id

@pytest.mark.asyncio
async def test_w188_get_not_found(client):
    r = await client.get("/api/audit-seal/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w188_verify_integrity(client):
    r = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    item_id = r.json()["seal_id"]
    r2 = await client.post(f"/api/audit-seal/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["seal_id"] == item_id

@pytest.mark.asyncio
async def test_w188_inject_tamper(client):
    r = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    item_id = r.json()["seal_id"]
    r2 = await client.post(f"/api/audit-seal/{item_id}/tamper", json={})
    assert r2.status_code == 200
    assert r2.json()["seal_id"] == item_id

@pytest.mark.asyncio
async def test_w188_detect_tamper(client):
    r = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    item_id = r.json()["seal_id"]
    r2 = await client.post(f"/api/audit-seal/{item_id}/detect", json={})
    assert r2.status_code == 200
    assert r2.json()["seal_id"] == item_id

@pytest.mark.asyncio
async def test_w188_verify_integrity_not_found(client):
    r = await client.post("/api/audit-seal/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w188_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "audit_seal"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w188_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "seal_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w188_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/audit-seal", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w188_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/audit-seal", json={'scope': 'test-scope', 'merkle_root': 'test-merkle_root', 'tool_trace_included': True, 'session_events_included': True, 'node_count': 1, 'integrity_status': 'test-integrity_status', 'tamper_detected': True, 'tampered_nodes': [], 'proof_artifact': {}, 'status': 'test-status', 'sealed_at': 'test-sealed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["seal_id"]
    r2 = await client.get("/api/audit-seal")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/audit-seal/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["seal_id"] == item_id
