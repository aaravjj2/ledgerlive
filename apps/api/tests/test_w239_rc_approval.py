"""Tests for Wave 239: RC Approval Chain v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w239_rc_approval import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w239_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w239_create(client):
    r = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "approval_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w239_list(client):
    await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    r = await client.get("/api/rc-approval")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w239_get_by_id(client):
    r = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    item_id = r.json()["approval_id"]
    r2 = await client.get(f"/api/rc-approval/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["approval_id"] == item_id

@pytest.mark.asyncio
async def test_w239_get_not_found(client):
    r = await client.get("/api/rc-approval/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w239_approve_level(client):
    r = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    item_id = r.json()["approval_id"]
    r2 = await client.post(f"/api/rc-approval/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["approval_id"] == item_id

@pytest.mark.asyncio
async def test_w239_reject_level(client):
    r = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    item_id = r.json()["approval_id"]
    r2 = await client.post(f"/api/rc-approval/{item_id}/reject", json={})
    assert r2.status_code == 200
    assert r2.json()["approval_id"] == item_id

@pytest.mark.asyncio
async def test_w239_delegate_approval(client):
    r = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    item_id = r.json()["approval_id"]
    r2 = await client.post(f"/api/rc-approval/{item_id}/delegate", json={})
    assert r2.status_code == 200
    assert r2.json()["approval_id"] == item_id

@pytest.mark.asyncio
async def test_w239_approve_level_not_found(client):
    r = await client.post("/api/rc-approval/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w239_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_approval"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w239_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "approval_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w239_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-approval", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w239_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-approval", json={'period_id': 'test-period_id', 'approval_level': 1, 'total_levels': 1, 'approvers': [], 'decisions': [], 'current_approver': 'test-current_approver', 'delegated_to': 'test-delegated_to', 'expires_at': 'test-expires_at', 'all_approved': True, 'rejection_reason': 'test-rejection_reason', 'status': 'test-status', 'initiated_at': 'test-initiated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["approval_id"]
    r2 = await client.get("/api/rc-approval")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-approval/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["approval_id"] == item_id
