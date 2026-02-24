"""Tests for Wave 320: Race Theme Pack v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w320_race_theme_pack_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w320_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w320_create(client):
    r = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "theme_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w320_list(client):
    await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/race-theme-pack-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w320_get_by_id(client):
    r = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["theme_id"]
    r2 = await client.get(f"/api/race-theme-pack-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["theme_id"] == item_id

@pytest.mark.asyncio
async def test_w320_get_not_found(client):
    r = await client.get("/api/race-theme-pack-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w320_check_consistency(client):
    r = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["theme_id"]
    r2 = await client.post(f"/api/race-theme-pack-v2/{item_id}/check", json={})
    assert r2.status_code == 200
    assert r2.json()["theme_id"] == item_id

@pytest.mark.asyncio
async def test_w320_apply_fixes(client):
    r = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["theme_id"]
    r2 = await client.post(f"/api/race-theme-pack-v2/{item_id}/fix", json={})
    assert r2.status_code == 200
    assert r2.json()["theme_id"] == item_id

@pytest.mark.asyncio
async def test_w320_check_consistency_not_found(client):
    r = await client.post("/api/race-theme-pack-v2/nonexistent-id/check", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w320_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "race_theme_pack_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w320_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "theme_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w320_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/race-theme-pack-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w320_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/race-theme-pack-v2", json={'theme_name': 'test-theme_name', 'naming_rules': [], 'inconsistencies_found': [], 'is_consistent': True, 'bundle_refs_checked': [], 'ui_refs_checked': [], 'fix_suggestions': [], 'theme_version': 1, 'deterministic': True, 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["theme_id"]
    r2 = await client.get("/api/race-theme-pack-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/race-theme-pack-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["theme_id"] == item_id
