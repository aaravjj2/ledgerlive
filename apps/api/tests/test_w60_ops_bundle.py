"""Tests for Wave 60: Enterprise Ops Bundle

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w60_ops_bundle import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w60_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w60_create(client):
    r = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    assert r.status_code == 201
    data = r.json()
    assert "bundle_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w60_list(client):
    await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    r = await client.get("/api/ops-bundles")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w60_get_by_id(client):
    r = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.get(f"/api/ops-bundles/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w60_get_not_found(client):
    r = await client.get("/api/ops-bundles/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w60_add_evidence(client):
    r = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/ops-bundles/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w60_compute_hash(client):
    r = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/ops-bundles/{item_id}/hash", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w60_verify_bundle(client):
    r = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/ops-bundles/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w60_add_evidence_not_found(client):
    r = await client.post("/api/ops-bundles/nonexistent-id/evidence", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w60_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ops_bundle"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w60_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "bundle_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w60_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ops-bundles", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w60_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/ops-bundles", json={'name': 'test-name', 'period_id': 'test-period_id', 'job_runs': [], 'alerts': [], 'quality_scores': {}, 'lineage': [], 'proof_index': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at', 'exported_at': 'test-exported_at'})
    assert r1.status_code == 201
    item_id = r1.json()["bundle_id"]
    r2 = await client.get("/api/ops-bundles")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ops-bundles/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["bundle_id"] == item_id
