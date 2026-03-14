"""Tests for Wave 336: One Cockpit v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w336_one_cockpit import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w336_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w336_create(client):
    r = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "cockpit_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w336_list(client):
    await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    r = await client.get("/api/one-cockpit")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w336_get_by_id(client):
    r = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    item_id = r.json()["cockpit_id"]
    r2 = await client.get(f"/api/one-cockpit/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["cockpit_id"] == item_id

@pytest.mark.asyncio
async def test_w336_get_not_found(client):
    r = await client.get("/api/one-cockpit/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w336_set_default(client):
    r = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    item_id = r.json()["cockpit_id"]
    r2 = await client.post(f"/api/one-cockpit/{item_id}/set-default", json={})
    assert r2.status_code == 200
    assert r2.json()["cockpit_id"] == item_id

@pytest.mark.asyncio
async def test_w336_customize_layout(client):
    r = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    item_id = r.json()["cockpit_id"]
    r2 = await client.post(f"/api/one-cockpit/{item_id}/customize", json={})
    assert r2.status_code == 200
    assert r2.json()["cockpit_id"] == item_id

@pytest.mark.asyncio
async def test_w336_set_default_not_found(client):
    r = await client.post("/api/one-cockpit/nonexistent-id/set-default", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w336_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "one_cockpit"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w336_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "cockpit_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w336_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/one-cockpit", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w336_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/one-cockpit", json={'layout_config': {}, 'visible_sections': [], 'hidden_sections': [], 'default_route': 'test-default_route', 'cognitive_load_score': 1.0, 'section_order': [], 'user_prefs': {}, 'is_home': True, 'deterministic': True, 'status': 'test-status', 'configured_at': 'test-configured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["cockpit_id"]
    r2 = await client.get("/api/one-cockpit")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/one-cockpit/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["cockpit_id"] == item_id
