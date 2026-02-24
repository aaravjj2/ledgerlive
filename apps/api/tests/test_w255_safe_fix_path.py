"""Tests for Wave 255: Safe Fix Path v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w255_safe_fix_path import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w255_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w255_create(client):
    r = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "fix_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w255_list(client):
    await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    r = await client.get("/api/safe-fix-path")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w255_get_by_id(client):
    r = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.get(f"/api/safe-fix-path/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w255_get_not_found(client):
    r = await client.get("/api/safe-fix-path/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w255_approve_fix(client):
    r = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.post(f"/api/safe-fix-path/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w255_apply_fix(client):
    r = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.post(f"/api/safe-fix-path/{item_id}/apply", json={})
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w255_approve_fix_not_found(client):
    r = await client.post("/api/safe-fix-path/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w255_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "safe_fix_path"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w255_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "fix_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w255_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/safe-fix-path", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w255_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/safe-fix-path", json={'blocked_action_ref': 'test-blocked_action_ref', 'block_reason': 'test-block_reason', 'remediation_steps': [], 'evidence_refs': [], 'risk_reduction_pct': 1.0, 'side_effects': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'applied': True, 'fix_hash': 'test-fix_hash', 'status': 'test-status', 'suggested_at': 'test-suggested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["fix_id"]
    r2 = await client.get("/api/safe-fix-path")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/safe-fix-path/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["fix_id"] == item_id
