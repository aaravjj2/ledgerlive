"""Tests for Wave 40: Evidence Binder 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w40_evidence_binder_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w40_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w40_create(client):
    r = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert r.status_code == 201
    data = r.json()
    assert "binder_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w40_list(client):
    await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    r = await client.get("/api/binders-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w40_get_by_id(client):
    r = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.get(f"/api/binders-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w40_get_not_found(client):
    r = await client.get("/api/binders-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w40_add_provenance(client):
    r = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.post(f"/api/binders-v2/{item_id}/provenance", json={})
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w40_sign_binder(client):
    r = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.post(f"/api/binders-v2/{item_id}/sign", json={})
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w40_verify_binder(client):
    r = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.post(f"/api/binders-v2/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w40_add_provenance_not_found(client):
    r = await client.post("/api/binders-v2/nonexistent-id/provenance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w40_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "evidence_binder_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w40_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "binder_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w40_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/binders-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w40_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/binders-v2", json={'period_id': 'test-period_id', 'title': 'test-title', 'controls_report': {}, 'approvals_chain': [], 'provenance': {}, 'merkle_root': 'test-merkle_root', 'signature': 'test-signature', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert r1.status_code == 201
    item_id = r1.json()["binder_id"]
    r2 = await client.get("/api/binders-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/binders-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["binder_id"] == item_id
