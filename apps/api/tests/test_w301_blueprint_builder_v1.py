"""Tests for Wave 301: Blueprint Builder v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w301_blueprint_builder_v1 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w301_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w301_create(client):
    r = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "blueprint_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w301_list(client):
    await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/blueprint-builder")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w301_get_by_id(client):
    r = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["blueprint_id"]
    r2 = await client.get(f"/api/blueprint-builder/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["blueprint_id"] == item_id

@pytest.mark.asyncio
async def test_w301_get_not_found(client):
    r = await client.get("/api/blueprint-builder/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w301_add_step(client):
    r = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["blueprint_id"]
    r2 = await client.post(f"/api/blueprint-builder/{item_id}/add-step", json={})
    assert r2.status_code == 200
    assert r2.json()["blueprint_id"] == item_id

@pytest.mark.asyncio
async def test_w301_set_policy(client):
    r = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["blueprint_id"]
    r2 = await client.post(f"/api/blueprint-builder/{item_id}/policy", json={})
    assert r2.status_code == 200
    assert r2.json()["blueprint_id"] == item_id

@pytest.mark.asyncio
async def test_w301_export_blueprint(client):
    r = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["blueprint_id"]
    r2 = await client.post(f"/api/blueprint-builder/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["blueprint_id"] == item_id

@pytest.mark.asyncio
async def test_w301_add_step_not_found(client):
    r = await client.post("/api/blueprint-builder/nonexistent-id/add-step", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w301_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "blueprint_builder_v1"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w301_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "blueprint_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w301_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/blueprint-builder", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w301_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/blueprint-builder", json={'name': 'test-name', 'steps': [], 'approval_policies': [], 'step_count': 1, 'has_approvals': True, 'export_format': 'test-export_format', 'export_checksum': 'test-export_checksum', 'version': 1, 'created_by': 'test-created_by', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["blueprint_id"]
    r2 = await client.get("/api/blueprint-builder")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/blueprint-builder/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["blueprint_id"] == item_id
