"""Tests for Wave 98: Execution Lineage

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w098_execution_lineage import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w098_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w098_create(client):
    r = await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "lineage_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w098_list(client):
    await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    r = await client.get("/api/execution-lineage")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w098_get_by_id(client):
    r = await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["lineage_id"]
    r2 = await client.get(f"/api/execution-lineage/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["lineage_id"] == item_id

@pytest.mark.asyncio
async def test_w098_get_not_found(client):
    r = await client.get("/api/execution-lineage/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w098_verify_lineage(client):
    r = await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["lineage_id"]
    r2 = await client.post(f"/api/execution-lineage/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["lineage_id"] == item_id

@pytest.mark.asyncio
async def test_w098_verify_lineage_not_found(client):
    r = await client.post("/api/execution-lineage/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w098_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "execution_lineage"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w098_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "lineage_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w098_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/execution-lineage", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w098_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/execution-lineage", json={'execution_id': 'test-execution_id', 'template_id': 'test-template_id', 'input_hash': 'test-input_hash', 'output_hash': 'test-output_hash', 'steps': [], 'provenance': {}, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["lineage_id"]
    r2 = await client.get("/api/execution-lineage")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/execution-lineage/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["lineage_id"] == item_id
