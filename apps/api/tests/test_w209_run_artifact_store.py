"""Tests for Wave 209: Run Artifact Store v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w209_run_artifact_store import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w209_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w209_create(client):
    r = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    assert r.status_code == 201
    data = r.json()
    assert "artifact_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w209_list(client):
    await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    r = await client.get("/api/run-artifacts")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w209_get_by_id(client):
    r = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    item_id = r.json()["artifact_id"]
    r2 = await client.get(f"/api/run-artifacts/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["artifact_id"] == item_id

@pytest.mark.asyncio
async def test_w209_get_not_found(client):
    r = await client.get("/api/run-artifacts/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w209_verify_manifest(client):
    r = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    item_id = r.json()["artifact_id"]
    r2 = await client.post(f"/api/run-artifacts/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["artifact_id"] == item_id

@pytest.mark.asyncio
async def test_w209_restore_snapshot(client):
    r = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    item_id = r.json()["artifact_id"]
    r2 = await client.post(f"/api/run-artifacts/{item_id}/restore", json={})
    assert r2.status_code == 200
    assert r2.json()["artifact_id"] == item_id

@pytest.mark.asyncio
async def test_w209_verify_manifest_not_found(client):
    r = await client.post("/api/run-artifacts/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w209_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "run_artifact_store"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w209_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "artifact_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w209_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/run-artifacts", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w209_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/run-artifacts", json={'close_period_id': 'test-close_period_id', 'artifact_type': 'test-artifact_type', 'content_address': 'test-content_address', 'version': 1, 'doc_hashes': [], 'ocr_hashes': [], 'extraction_outputs': {}, 'transactions_snapshot': {}, 'tool_plan_ref': 'test-tool_plan_ref', 'tool_trace_ref': 'test-tool_trace_ref', 'approvals_snapshot': [], 'manifest_hash': 'test-manifest_hash', 'status': 'test-status', 'stored_at': 'test-stored_at'})
    assert r1.status_code == 201
    item_id = r1.json()["artifact_id"]
    r2 = await client.get("/api/run-artifacts")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/run-artifacts/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["artifact_id"] == item_id
