"""Tests for Wave 242: Plan Preview v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w242_plan_preview import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w242_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w242_create(client):
    r = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "plan_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w242_list(client):
    await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    r = await client.get("/api/plan-preview")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w242_get_by_id(client):
    r = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    item_id = r.json()["plan_id"]
    r2 = await client.get(f"/api/plan-preview/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["plan_id"] == item_id

@pytest.mark.asyncio
async def test_w242_get_not_found(client):
    r = await client.get("/api/plan-preview/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w242_validate_plan(client):
    r = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    item_id = r.json()["plan_id"]
    r2 = await client.post(f"/api/plan-preview/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["plan_id"] == item_id

@pytest.mark.asyncio
async def test_w242_predict_hashes(client):
    r = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    item_id = r.json()["plan_id"]
    r2 = await client.post(f"/api/plan-preview/{item_id}/predict-hashes", json={})
    assert r2.status_code == 200
    assert r2.json()["plan_id"] == item_id

@pytest.mark.asyncio
async def test_w242_validate_plan_not_found(client):
    r = await client.post("/api/plan-preview/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w242_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "plan_preview"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w242_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "plan_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w242_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/plan-preview", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w242_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/plan-preview", json={'plan_name': 'test-plan_name', 'action_sequence': [], 'predicted_artifacts': [], 'predicted_hashes': {}, 'estimated_duration_min': 1, 'risk_assessment': {}, 'prerequisites_met': True, 'side_effects': [], 'approval_required': True, 'deterministic_hash': 'test-deterministic_hash', 'status': 'test-status', 'previewed_at': 'test-previewed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["plan_id"]
    r2 = await client.get("/api/plan-preview")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/plan-preview/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["plan_id"] == item_id
