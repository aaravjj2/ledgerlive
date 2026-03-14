"""Tests for Wave 36: Accruals & Deferrals

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w36_accruals_deferrals import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w36_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w36_create(client):
    r = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "schedule_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w36_list(client):
    await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    r = await client.get("/api/accruals")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w36_get_by_id(client):
    r = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.get(f"/api/accruals/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w36_get_not_found(client):
    r = await client.get("/api/accruals/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w36_generate_proposal(client):
    r = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.post(f"/api/accruals/{item_id}/propose", json={})
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w36_approve_proposal(client):
    r = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.post(f"/api/accruals/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w36_reverse(client):
    r = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.post(f"/api/accruals/{item_id}/reverse", json={})
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w36_generate_proposal_not_found(client):
    r = await client.post("/api/accruals/nonexistent-id/propose", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w36_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "accruals_deferrals"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w36_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "schedule_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w36_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/accruals", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w36_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/accruals", json={'name': 'test-name', 'schedule_type': 'test-schedule_type', 'amount': 1.0, 'frequency': 'test-frequency', 'start_date': 'test-start_date', 'end_date': 'test-end_date', 'status': 'test-status', 'auto_reverse': True, 'approved_by': 'test-approved_by', 'next_run': 'test-next_run', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["schedule_id"]
    r2 = await client.get("/api/accruals")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/accruals/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["schedule_id"] == item_id
