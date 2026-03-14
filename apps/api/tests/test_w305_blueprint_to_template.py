"""Tests for Wave 305: Blueprint-to-Template Compiler v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w305_blueprint_to_template import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w305_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w305_create(client):
    r = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    assert r.status_code == 201
    data = r.json()
    assert "compile_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w305_list(client):
    await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    r = await client.get("/api/blueprint-to-template")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w305_get_by_id(client):
    r = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    item_id = r.json()["compile_id"]
    r2 = await client.get(f"/api/blueprint-to-template/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["compile_id"] == item_id

@pytest.mark.asyncio
async def test_w305_get_not_found(client):
    r = await client.get("/api/blueprint-to-template/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w305_validate_output(client):
    r = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    item_id = r.json()["compile_id"]
    r2 = await client.post(f"/api/blueprint-to-template/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["compile_id"] == item_id

@pytest.mark.asyncio
async def test_w305_recompile(client):
    r = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    item_id = r.json()["compile_id"]
    r2 = await client.post(f"/api/blueprint-to-template/{item_id}/recompile", json={})
    assert r2.status_code == 200
    assert r2.json()["compile_id"] == item_id

@pytest.mark.asyncio
async def test_w305_validate_output_not_found(client):
    r = await client.post("/api/blueprint-to-template/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w305_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "blueprint_to_template"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w305_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "compile_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w305_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/blueprint-to-template", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w305_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/blueprint-to-template", json={'blueprint_ref': 'test-blueprint_ref', 'template_output': {}, 'artifact_manifest': [], 'compilation_log': [], 'warnings': [], 'errors': [], 'output_checksum': 'test-output_checksum', 'compiler_version': 'test-compiler_version', 'deterministic': True, 'status': 'test-status', 'compiled_at': 'test-compiled_at'})
    assert r1.status_code == 201
    item_id = r1.json()["compile_id"]
    r2 = await client.get("/api/blueprint-to-template")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/blueprint-to-template/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["compile_id"] == item_id
