"""Tests for Wave 178: Airia Adapter Skeleton

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w178_airia_adapter import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w178_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w178_create(client):
    r = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "package_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w178_list(client):
    await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/airia-adapter")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w178_get_by_id(client):
    r = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["package_id"]
    r2 = await client.get(f"/api/airia-adapter/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["package_id"] == item_id

@pytest.mark.asyncio
async def test_w178_get_not_found(client):
    r = await client.get("/api/airia-adapter/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w178_validate_package(client):
    r = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["package_id"]
    r2 = await client.post(f"/api/airia-adapter/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["package_id"] == item_id

@pytest.mark.asyncio
async def test_w178_export_package(client):
    r = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["package_id"]
    r2 = await client.post(f"/api/airia-adapter/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["package_id"] == item_id

@pytest.mark.asyncio
async def test_w178_validate_package_not_found(client):
    r = await client.post("/api/airia-adapter/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w178_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "airia_adapter"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w178_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "package_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w178_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/airia-adapter", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w178_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/airia-adapter", json={'package_name': 'test-package_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'screenshots_list': [], 'metadata': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["package_id"]
    r2 = await client.get("/api/airia-adapter")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/airia-adapter/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["package_id"] == item_id
