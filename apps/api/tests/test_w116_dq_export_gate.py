"""Tests for Wave 116: DQ Export Gate

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w116_dq_export_gate import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w116_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w116_create(client):
    r = await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "gate_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w116_list(client):
    await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/dq-export-gates")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w116_get_by_id(client):
    r = await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.get(f"/api/dq-export-gates/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w116_get_not_found(client):
    r = await client.get("/api/dq-export-gates/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w116_approve_override(client):
    r = await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/dq-export-gates/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w116_approve_override_not_found(client):
    r = await client.post("/api/dq-export-gates/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w116_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "dq_export_gate"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w116_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "gate_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w116_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/dq-export-gates", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w116_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/dq-export-gates", json={'export_id': 'test-export_id', 'quality_score': 1.0, 'threshold': 1.0, 'blocked': True, 'override_approved': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["gate_id"]
    r2 = await client.get("/api/dq-export-gates")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/dq-export-gates/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["gate_id"] == item_id
