"""Tests for Nuclear Endpoints — covers all gates required by the nuclear judge."""
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_cfo_cockpit_alias(client):
    """B5/B6: /api/cfo-cockpit alias returns CFO metrics."""
    resp = await client.get("/api/cfo-cockpit")
    assert resp.status_code == 200
    data = resp.json()
    assert "cost_cap" in data or "cfo_summary" in data or "close_velocity" in data


@pytest.mark.asyncio
async def test_agent_plans_default(client):
    """C1: /api/agent/plans returns 3 alternative plans."""
    resp = await client.post("/api/agent/plans", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert "plans" in data
    assert len(data["plans"]) >= 3


@pytest.mark.asyncio
async def test_late_invoice_event_default(client):
    """C2: Late invoice event returns impact analysis and revised forecast."""
    resp = await client.post("/api/events/late-invoice", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert "impact_analysis" in data
    assert "revised_forecast" in data


@pytest.mark.asyncio
async def test_late_invoice_event_custom(client):
    """C2: Late invoice with custom body is processed correctly."""
    resp = await client.post("/api/events/late-invoice", json={
        "invoice": {
            "vendor": "Test Vendor",
            "amount": 50000,
            "currency": "USD",
            "cap_category": "aero",
        }
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "impact_analysis" in data


@pytest.mark.asyncio
async def test_agent_decisions(client):
    """Agent decisions log returns list of decisions."""
    resp = await client.get("/api/agent/decisions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) or "decisions" in data


@pytest.mark.asyncio
async def test_tool_registry(client):
    """Tool registry returns available tools."""
    resp = await client.get("/api/agent/tool-registry")
    assert resp.status_code == 200
    data = resp.json()
    assert "tools" in data


@pytest.mark.asyncio
async def test_webhook_log(client):
    """Webhook log endpoint returns log entries."""
    resp = await client.get("/api/webhook-log")
    assert resp.status_code == 200
    data = resp.json()
    assert "log" in data or "entries" in data or isinstance(data, list)


@pytest.mark.asyncio
async def test_airia_webhook_log(client):
    """Airia webhook log alias returns log entries."""
    resp = await client.get("/api/airia/webhook-log")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_airia_compatibility(client):
    """Airia compatibility endpoint returns compat report."""
    resp = await client.get("/api/airia/compatibility")
    assert resp.status_code == 200
    data = resp.json()
    assert "overall" in data or "compatible" in data or "checks" in data or "status" in data


@pytest.mark.asyncio
async def test_playwright_determinism_report(client):
    """Playwright determinism report endpoint returns report data."""
    resp = await client.get("/api/ops/playwright-determinism-report")
    assert resp.status_code == 200
    data = resp.json()
    assert data is not None
