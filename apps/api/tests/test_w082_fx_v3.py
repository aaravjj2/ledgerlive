"""Tests for Wave 82: FX Translation 3.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w082_fx_v3 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w082_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w082_create(client):
    r = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "translation_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w082_list(client):
    await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/fx-v3/translations")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w082_get_by_id(client):
    r = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["translation_id"]
    r2 = await client.get(f"/api/fx-v3/translations/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["translation_id"] == item_id

@pytest.mark.asyncio
async def test_w082_get_not_found(client):
    r = await client.get("/api/fx-v3/translations/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w082_snapshot_rates(client):
    r = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["translation_id"]
    r2 = await client.post(f"/api/fx-v3/translations/{item_id}/snapshot", json={})
    assert r2.status_code == 200
    assert r2.json()["translation_id"] == item_id

@pytest.mark.asyncio
async def test_w082_compute_cta(client):
    r = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["translation_id"]
    r2 = await client.post(f"/api/fx-v3/translations/{item_id}/cta", json={})
    assert r2.status_code == 200
    assert r2.json()["translation_id"] == item_id

@pytest.mark.asyncio
async def test_w082_snapshot_rates_not_found(client):
    r = await client.post("/api/fx-v3/translations/nonexistent-id/snapshot", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w082_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "fx_v3"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w082_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "translation_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w082_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/fx-v3/translations", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w082_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/fx-v3/translations", json={'source_currency': 'test-source_currency', 'target_currency': 'test-target_currency', 'rate': 1.0, 'rate_date': 'test-rate_date', 'rate_source': 'test-rate_source', 'cta_amount': 1.0, 'translated_amount': 1.0, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["translation_id"]
    r2 = await client.get("/api/fx-v3/translations")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/fx-v3/translations/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["translation_id"] == item_id
