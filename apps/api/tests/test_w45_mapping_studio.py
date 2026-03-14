"""Tests for Wave 45: Mapping Studio 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w45_mapping_studio import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w45_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w45_create(client):
    r = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "rule_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w45_list(client):
    await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    r = await client.get("/api/mapping-studio/rules")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w45_get_by_id(client):
    r = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.get(f"/api/mapping-studio/rules/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w45_get_not_found(client):
    r = await client.get("/api/mapping-studio/rules/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w45_preview(client):
    r = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/mapping-studio/rules/{item_id}/preview", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w45_apply_rule(client):
    r = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/mapping-studio/rules/{item_id}/apply", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w45_rollback(client):
    r = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/mapping-studio/rules/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w45_preview_not_found(client):
    r = await client.post("/api/mapping-studio/rules/nonexistent-id/preview", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w45_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "mapping_studio"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w45_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "rule_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w45_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/mapping-studio/rules", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w45_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/mapping-studio/rules", json={'name': 'test-name', 'rule_type': 'test-rule_type', 'source_field': 'test-source_field', 'target_field': 'test-target_field', 'transform_expr': 'test-transform_expr', 'priority': 1, 'active': True, 'version': 1, 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["rule_id"]
    r2 = await client.get("/api/mapping-studio/rules")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/mapping-studio/rules/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["rule_id"] == item_id
