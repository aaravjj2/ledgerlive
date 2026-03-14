"""Tests for Wave 198: Deployed Environment Chaos Hooks

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w198_chaos_hooks import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w198_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w198_create(client):
    r = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "hook_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w198_list(client):
    await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/chaos-hooks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w198_get_by_id(client):
    r = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["hook_id"]
    r2 = await client.get(f"/api/chaos-hooks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["hook_id"] == item_id

@pytest.mark.asyncio
async def test_w198_get_not_found(client):
    r = await client.get("/api/chaos-hooks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w198_validate_hook(client):
    r = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["hook_id"]
    r2 = await client.post(f"/api/chaos-hooks/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["hook_id"] == item_id

@pytest.mark.asyncio
async def test_w198_check_ci_safety(client):
    r = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["hook_id"]
    r2 = await client.post(f"/api/chaos-hooks/{item_id}/ci-check", json={})
    assert r2.status_code == 200
    assert r2.json()["hook_id"] == item_id

@pytest.mark.asyncio
async def test_w198_validate_hook_not_found(client):
    r = await client.post("/api/chaos-hooks/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w198_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "chaos_hooks"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w198_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "hook_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w198_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/chaos-hooks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w198_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/chaos-hooks", json={'hook_name': 'test-hook_name', 'target_env': 'test-target_env', 'chaos_seed': 1, 'chaos_scenarios': [], 'script_path': 'test-script_path', 'script_valid': True, 'ci_safe': True, 'never_in_ci': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["hook_id"]
    r2 = await client.get("/api/chaos-hooks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/chaos-hooks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["hook_id"] == item_id
