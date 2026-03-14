"""Tests for Wave 58: KPI Framework

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w58_kpi_framework import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w58_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w58_create(client):
    r = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "kpi_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w58_list(client):
    await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    r = await client.get("/api/kpis")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w58_get_by_id(client):
    r = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    item_id = r.json()["kpi_id"]
    r2 = await client.get(f"/api/kpis/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["kpi_id"] == item_id

@pytest.mark.asyncio
async def test_w58_get_not_found(client):
    r = await client.get("/api/kpis/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w58_compute(client):
    r = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    item_id = r.json()["kpi_id"]
    r2 = await client.post(f"/api/kpis/{item_id}/compute", json={})
    assert r2.status_code == 200
    assert r2.json()["kpi_id"] == item_id

@pytest.mark.asyncio
async def test_w58_link_evidence(client):
    r = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    item_id = r.json()["kpi_id"]
    r2 = await client.post(f"/api/kpis/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["kpi_id"] == item_id

@pytest.mark.asyncio
async def test_w58_compute_not_found(client):
    r = await client.post("/api/kpis/nonexistent-id/compute", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w58_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "kpi_framework"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w58_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "kpi_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w58_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/kpis", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w58_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/kpis", json={'name': 'test-name', 'formula': 'test-formula', 'value': 1.0, 'target': 1.0, 'unit': 'test-unit', 'evidence_links': [], 'status': 'test-status', 'owner': 'test-owner', 'computed_at': 'test-computed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["kpi_id"]
    r2 = await client.get("/api/kpis")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/kpis/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["kpi_id"] == item_id
