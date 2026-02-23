"""Tests for Wave 111: Data Lake Export 3.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w111_data_lake_export import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w111_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w111_create(client):
    r = await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r.status_code == 201
    data = r.json()
    assert "export_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w111_list(client):
    await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    r = await client.get("/api/data-lake-exports")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w111_get_by_id(client):
    r = await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.get(f"/api/data-lake-exports/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w111_get_not_found(client):
    r = await client.get("/api/data-lake-exports/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w111_verify_export(client):
    r = await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["export_id"]
    r2 = await client.post(f"/api/data-lake-exports/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w111_verify_export_not_found(client):
    r = await client.post("/api/data-lake-exports/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w111_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "data_lake_export"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w111_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "export_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w111_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/data-lake-exports", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w111_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/data-lake-exports", json={'format_type': 'test-format_type', 'schema_version': 'test-schema_version', 'record_count': 1, 'file_size_bytes': 1, 'schema_snapshot': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r1.status_code == 201
    item_id = r1.json()["export_id"]
    r2 = await client.get("/api/data-lake-exports")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/data-lake-exports/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["export_id"] == item_id
