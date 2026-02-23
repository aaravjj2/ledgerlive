"""Tests for Wave 171: ML Dataset Builder v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w171_ml_dataset import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w171_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w171_create(client):
    r = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "dataset_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w171_list(client):
    await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/ml-datasets")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w171_get_by_id(client):
    r = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["dataset_id"]
    r2 = await client.get(f"/api/ml-datasets/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["dataset_id"] == item_id

@pytest.mark.asyncio
async def test_w171_get_not_found(client):
    r = await client.get("/api/ml-datasets/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w171_verify_dataset(client):
    r = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["dataset_id"]
    r2 = await client.post(f"/api/ml-datasets/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["dataset_id"] == item_id

@pytest.mark.asyncio
async def test_w171_export_dataset(client):
    r = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["dataset_id"]
    r2 = await client.post(f"/api/ml-datasets/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["dataset_id"] == item_id

@pytest.mark.asyncio
async def test_w171_verify_dataset_not_found(client):
    r = await client.post("/api/ml-datasets/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w171_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ml_dataset"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w171_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "dataset_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w171_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ml-datasets", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w171_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/ml-datasets", json={'dataset_name': 'test-dataset_name', 'dataset_type': 'test-dataset_type', 'record_count': 1, 'label_count': 1, 'seed': 1, 'content_hash': 'test-content_hash', 'manifest': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["dataset_id"]
    r2 = await client.get("/api/ml-datasets")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ml-datasets/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["dataset_id"] == item_id
