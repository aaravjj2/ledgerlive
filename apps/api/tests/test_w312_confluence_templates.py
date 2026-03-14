"""Tests for Wave 312: Confluence Page Templates v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w312_confluence_templates import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w312_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w312_create(client):
    r = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    assert r.status_code == 201
    data = r.json()
    assert "template_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w312_list(client):
    await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    r = await client.get("/api/confluence-templates")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w312_get_by_id(client):
    r = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    item_id = r.json()["template_id"]
    r2 = await client.get(f"/api/confluence-templates/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["template_id"] == item_id

@pytest.mark.asyncio
async def test_w312_get_not_found(client):
    r = await client.get("/api/confluence-templates/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w312_render_template(client):
    r = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    item_id = r.json()["template_id"]
    r2 = await client.post(f"/api/confluence-templates/{item_id}/render", json={})
    assert r2.status_code == 200
    assert r2.json()["template_id"] == item_id

@pytest.mark.asyncio
async def test_w312_validate_citations(client):
    r = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    item_id = r.json()["template_id"]
    r2 = await client.post(f"/api/confluence-templates/{item_id}/citations", json={})
    assert r2.status_code == 200
    assert r2.json()["template_id"] == item_id

@pytest.mark.asyncio
async def test_w312_render_template_not_found(client):
    r = await client.post("/api/confluence-templates/nonexistent-id/render", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w312_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "confluence_templates"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w312_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "template_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w312_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/confluence-templates", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w312_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/confluence-templates", json={'template_name': 'test-template_name', 'template_body': 'test-template_body', 'citation_refs': [], 'dossier_refs': [], 'evidence_refs': [], 'rendered_output': 'test-rendered_output', 'render_checksum': 'test-render_checksum', 'variable_slots': [], 'deterministic': True, 'status': 'test-status', 'rendered_at': 'test-rendered_at'})
    assert r1.status_code == 201
    item_id = r1.json()["template_id"]
    r2 = await client.get("/api/confluence-templates")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/confluence-templates/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["template_id"] == item_id
