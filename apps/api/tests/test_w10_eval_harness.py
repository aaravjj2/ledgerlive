"""Tests for Wave 10: Eval Harness

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w10_eval_harness import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w10_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w10_create(client):
    r = await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    assert r.status_code == 201
    data = r.json()
    assert "eval_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w10_list(client):
    await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    r = await client.get("/api/evals")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w10_get_by_id(client):
    r = await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    item_id = r.json()["eval_id"]
    r2 = await client.get(f"/api/evals/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["eval_id"] == item_id

@pytest.mark.asyncio
async def test_w10_get_not_found(client):
    r = await client.get("/api/evals/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w10_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "eval_harness"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w10_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/evals", json={'eval_type': 'test-eval_type', 'dataset': 'test-dataset', 'precision': 1.0, 'recall': 1.0, 'f1_score': 1.0, 'run_at': 'test-run_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "eval_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w10_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/evals", json={})
    assert r.status_code == 201
