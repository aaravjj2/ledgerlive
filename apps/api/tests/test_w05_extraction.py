"""Tests for Wave 5: Data Extraction

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w05_extraction import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w05_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w05_create(client):
    r = await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    assert r.status_code == 201
    data = r.json()
    assert "extraction_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w05_list(client):
    await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    r = await client.get("/api/extractions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w05_get_by_id(client):
    r = await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    item_id = r.json()["extraction_id"]
    r2 = await client.get(f"/api/extractions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["extraction_id"] == item_id

@pytest.mark.asyncio
async def test_w05_get_not_found(client):
    r = await client.get("/api/extractions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w05_update(client):
    r = await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    item_id = r.json()["extraction_id"]
    r2 = await client.put(f"/api/extractions/{item_id}", json={"name": "updated"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"

@pytest.mark.asyncio
async def test_w05_validate(client):
    r = await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    item_id = r.json()["extraction_id"]
    r2 = await client.post(f"/api/extractions/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["extraction_id"] == item_id

@pytest.mark.asyncio
async def test_w05_validate_not_found(client):
    r = await client.post("/api/extractions/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w05_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "extraction"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w05_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/extractions", json={'ocr_id': 'test-ocr_id', 'doc_type': 'test-doc_type', 'vendor_name': 'test-vendor_name', 'amount': 1.0, 'currency': 'test-currency', 'invoice_date': 'test-invoice_date', 'due_date': 'test-due_date', 'line_items': []})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "extraction_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w05_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/extractions", json={})
    assert r.status_code == 201
