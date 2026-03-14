"""Tests for Wave 168: Hackpack Generator v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w168_hackpack_gen import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w168_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w168_create(client):
    r = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "hackpack_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w168_list(client):
    await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/hackpacks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w168_get_by_id(client):
    r = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["hackpack_id"]
    r2 = await client.get(f"/api/hackpacks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["hackpack_id"] == item_id

@pytest.mark.asyncio
async def test_w168_get_not_found(client):
    r = await client.get("/api/hackpacks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w168_validate_hackpack(client):
    r = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["hackpack_id"]
    r2 = await client.post(f"/api/hackpacks/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["hackpack_id"] == item_id

@pytest.mark.asyncio
async def test_w168_export_hackpack(client):
    r = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["hackpack_id"]
    r2 = await client.post(f"/api/hackpacks/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["hackpack_id"] == item_id

@pytest.mark.asyncio
async def test_w168_validate_hackpack_not_found(client):
    r = await client.post("/api/hackpacks/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w168_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "hackpack_gen"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w168_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "hackpack_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w168_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/hackpacks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w168_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/hackpacks", json={'pack_name': 'test-pack_name', 'architecture_ref': 'test-architecture_ref', 'tool_schemas': [], 'demo_script': 'test-demo_script', 'proof_pack_ref': 'test-proof_pack_ref', 'checksums': {}, 'content_hash': 'test-content_hash', 'deployment_placeholders': {}, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["hackpack_id"]
    r2 = await client.get("/api/hackpacks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/hackpacks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["hackpack_id"] == item_id
