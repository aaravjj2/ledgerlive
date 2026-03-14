"""Tests for Wave 218: Auto Architecture Diagram Generator v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w218_arch_diagram import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w218_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w218_create(client):
    r = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "diagram_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w218_list(client):
    await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/arch-diagrams")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w218_get_by_id(client):
    r = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["diagram_id"]
    r2 = await client.get(f"/api/arch-diagrams/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["diagram_id"] == item_id

@pytest.mark.asyncio
async def test_w218_get_not_found(client):
    r = await client.get("/api/arch-diagrams/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w218_validate_diagram(client):
    r = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["diagram_id"]
    r2 = await client.post(f"/api/arch-diagrams/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["diagram_id"] == item_id

@pytest.mark.asyncio
async def test_w218_export_diagram(client):
    r = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["diagram_id"]
    r2 = await client.post(f"/api/arch-diagrams/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["diagram_id"] == item_id

@pytest.mark.asyncio
async def test_w218_validate_diagram_not_found(client):
    r = await client.post("/api/arch-diagrams/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w218_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "arch_diagram"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w218_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "diagram_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w218_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/arch-diagrams", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w218_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/arch-diagrams", json={'diagram_name': 'test-diagram_name', 'source_format': 'test-source_format', 'routers_count': 1, 'tools_count': 1, 'workflow_nodes': 1, 'storage_components': [], 'source_content': 'test-source_content', 'content_hash': 'test-content_hash', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["diagram_id"]
    r2 = await client.get("/api/arch-diagrams")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/arch-diagrams/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["diagram_id"] == item_id
