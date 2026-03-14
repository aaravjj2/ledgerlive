"""Tests for Wave 97: Breaking Change Detector

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w097_breaking_change import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w097_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w097_create(client):
    r = await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert r.status_code == 201
    data = r.json()
    assert "detection_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w097_list(client):
    await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    r = await client.get("/api/breaking-changes")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w097_get_by_id(client):
    r = await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["detection_id"]
    r2 = await client.get(f"/api/breaking-changes/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["detection_id"] == item_id

@pytest.mark.asyncio
async def test_w097_get_not_found(client):
    r = await client.get("/api/breaking-changes/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w097_suggest_migration(client):
    r = await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    item_id = r.json()["detection_id"]
    r2 = await client.post(f"/api/breaking-changes/{item_id}/migrate", json={})
    assert r2.status_code == 200
    assert r2.json()["detection_id"] == item_id

@pytest.mark.asyncio
async def test_w097_suggest_migration_not_found(client):
    r = await client.post("/api/breaking-changes/nonexistent-id/migrate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w097_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "breaking_change"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w097_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "detection_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w097_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/breaking-changes", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w097_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/breaking-changes", json={'template_id': 'test-template_id', 'old_version': 'test-old_version', 'new_version': 'test-new_version', 'breaking_changes': [], 'severity': 'test-severity', 'auto_migratable': True, 'status': 'test-status', 'detected_at': 'test-detected_at'})
    assert r1.status_code == 201
    item_id = r1.json()["detection_id"]
    r2 = await client.get("/api/breaking-changes")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/breaking-changes/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["detection_id"] == item_id
