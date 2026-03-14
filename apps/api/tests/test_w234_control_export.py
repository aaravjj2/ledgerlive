"""Tests for Wave 234: Control Room Export v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w234_control_export import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w234_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w234_create(client):
    r = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r.status_code == 201
    data = r.json()
    assert "export_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w234_list(client):
    await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    r = await client.get("/api/control-export")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w234_get_by_id(client):
    r = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.get(f"/api/control-export/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w234_get_not_found(client):
    r = await client.get("/api/control-export/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w234_verify_hash(client):
    r = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.post(f"/api/control-export/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w234_download_export(client):
    r = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.post(f"/api/control-export/{item_id}/download", json={})
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w234_verify_hash_not_found(client):
    r = await client.post("/api/control-export/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w234_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "control_export"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w234_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "export_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w234_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/control-export", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w234_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/control-export", json={'period_id': 'test-period_id', 'snapshot_data': {}, 'lanes_snapshot': [], 'scoreboard_snapshot': {}, 'critical_path_snapshot': {}, 'incidents_snapshot': [], 'checkpoints_snapshot': [], 'content_hash': 'test-content_hash', 'export_format': 'test-export_format', 'deterministic': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r1.status_code == 201
    item_id = r1.json()["export_id"]
    r2 = await client.get("/api/control-export")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/control-export/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["export_id"] == item_id
