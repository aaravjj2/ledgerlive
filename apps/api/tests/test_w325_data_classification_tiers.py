"""Tests for Wave 325: Data Classification Tiers v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w325_data_classification_tiers import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w325_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w325_create(client):
    r = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "classification_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w325_list(client):
    await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    r = await client.get("/api/data-classification-tiers")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w325_get_by_id(client):
    r = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    item_id = r.json()["classification_id"]
    r2 = await client.get(f"/api/data-classification-tiers/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["classification_id"] == item_id

@pytest.mark.asyncio
async def test_w325_get_not_found(client):
    r = await client.get("/api/data-classification-tiers/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w325_enforce_policy(client):
    r = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    item_id = r.json()["classification_id"]
    r2 = await client.post(f"/api/data-classification-tiers/{item_id}/enforce", json={})
    assert r2.status_code == 200
    assert r2.json()["classification_id"] == item_id

@pytest.mark.asyncio
async def test_w325_reclassify(client):
    r = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    item_id = r.json()["classification_id"]
    r2 = await client.post(f"/api/data-classification-tiers/{item_id}/reclassify", json={})
    assert r2.status_code == 200
    assert r2.json()["classification_id"] == item_id

@pytest.mark.asyncio
async def test_w325_enforce_policy_not_found(client):
    r = await client.post("/api/data-classification-tiers/nonexistent-id/enforce", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w325_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "data_classification_tiers"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w325_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "classification_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w325_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/data-classification-tiers", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w325_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/data-classification-tiers", json={'document_ref': 'test-document_ref', 'field_name': 'test-field_name', 'tier': 'test-tier', 'tier_level': 1, 'policy_ref': 'test-policy_ref', 'enforcement_action': 'test-enforcement_action', 'is_enforced': True, 'display_label': 'test-display_label', 'classification_reason': 'test-classification_reason', 'deterministic': True, 'status': 'test-status', 'classified_at': 'test-classified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["classification_id"]
    r2 = await client.get("/api/data-classification-tiers")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/data-classification-tiers/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["classification_id"] == item_id
