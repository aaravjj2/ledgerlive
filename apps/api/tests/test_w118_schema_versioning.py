"""Tests for Wave 118: Schema Versioning

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w118_schema_versioning import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w118_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w118_create(client):
    r = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    assert r.status_code == 201
    data = r.json()
    assert "schema_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w118_list(client):
    await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    r = await client.get("/api/schema-versions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w118_get_by_id(client):
    r = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    item_id = r.json()["schema_id"]
    r2 = await client.get(f"/api/schema-versions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["schema_id"] == item_id

@pytest.mark.asyncio
async def test_w118_get_not_found(client):
    r = await client.get("/api/schema-versions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w118_apply_migration(client):
    r = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    item_id = r.json()["schema_id"]
    r2 = await client.post(f"/api/schema-versions/{item_id}/apply", json={})
    assert r2.status_code == 200
    assert r2.json()["schema_id"] == item_id

@pytest.mark.asyncio
async def test_w118_rollback_schema(client):
    r = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    item_id = r.json()["schema_id"]
    r2 = await client.post(f"/api/schema-versions/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["schema_id"] == item_id

@pytest.mark.asyncio
async def test_w118_apply_migration_not_found(client):
    r = await client.post("/api/schema-versions/nonexistent-id/apply", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w118_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "schema_versioning"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w118_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "schema_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w118_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/schema-versions", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w118_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/schema-versions", json={'schema_name': 'test-schema_name', 'version': 'test-version', 'migration_sql': 'test-migration_sql', 'rollback_sql': 'test-rollback_sql', 'applied': True, 'deterministic': True, 'status': 'test-status', 'released_at': 'test-released_at'})
    assert r1.status_code == 201
    item_id = r1.json()["schema_id"]
    r2 = await client.get("/api/schema-versions")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/schema-versions/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["schema_id"] == item_id
