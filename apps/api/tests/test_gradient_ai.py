"""Tests for Gradient AI and Spaces integration."""
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_gradient_metrics(client):
    resp = await client.get("/api/gradient/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert "documents_processed" in data
    assert "api_key_configured" in data


@pytest.mark.asyncio
async def test_gradient_extract_demo(client):
    resp = await client.post("/api/gradient/extract-demo")
    assert resp.status_code == 200
    data = resp.json()
    assert "text" in data
    assert "confidence" in data
    assert data["confidence"] >= 0.9
    assert "fields" in data


@pytest.mark.asyncio
async def test_storage_log(client):
    resp = await client.get("/api/gradient/storage-log")
    assert resp.status_code == 200
    data = resp.json()
    assert "operations" in data
