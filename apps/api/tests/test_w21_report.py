"""Tests for Wave 21: Report Generator

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w21_report import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w21_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w21_create(client):
    r = await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "report_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w21_list(client):
    await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/reports")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w21_get_by_id(client):
    r = await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["report_id"]
    r2 = await client.get(f"/api/reports/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["report_id"] == item_id

@pytest.mark.asyncio
async def test_w21_get_not_found(client):
    r = await client.get("/api/reports/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w21_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "report"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w21_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/reports", json={'name': 'test-name', 'report_type': 'test-report_type', 'period_id': 'test-period_id', 'format_type': 'test-format_type', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "report_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w21_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/reports", json={})
    assert r.status_code == 201
