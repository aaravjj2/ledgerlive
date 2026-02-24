"""Tests for Wave 245: Race Control Why v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w245_rc_why_dossier import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w245_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w245_create(client):
    r = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "why_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w245_list(client):
    await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/rc-why")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w245_get_by_id(client):
    r = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["why_id"]
    r2 = await client.get(f"/api/rc-why/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["why_id"] == item_id

@pytest.mark.asyncio
async def test_w245_get_not_found(client):
    r = await client.get("/api/rc-why/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w245_expand_reason(client):
    r = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["why_id"]
    r2 = await client.post(f"/api/rc-why/{item_id}/expand", json={})
    assert r2.status_code == 200
    assert r2.json()["why_id"] == item_id

@pytest.mark.asyncio
async def test_w245_verify_consistency(client):
    r = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["why_id"]
    r2 = await client.post(f"/api/rc-why/{item_id}/verify-consistency", json={})
    assert r2.status_code == 200
    assert r2.json()["why_id"] == item_id

@pytest.mark.asyncio
async def test_w245_expand_reason_not_found(client):
    r = await client.post("/api/rc-why/nonexistent-id/expand", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w245_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_why_dossier"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w245_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "why_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w245_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-why", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w245_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-why", json={'action_ref': 'test-action_ref', 'reason_dag': {}, 'evidence_chain': [], 'dossier_content': {}, 'policy_refs': [], 'precedent_refs': [], 'confidence_score': 1.0, 'surface_type': 'test-surface_type', 'render_hash': 'test-render_hash', 'consistent_across': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["why_id"]
    r2 = await client.get("/api/rc-why")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-why/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["why_id"] == item_id
