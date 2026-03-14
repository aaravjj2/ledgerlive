"""Tests for Gemini voice endpoints."""
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_voice_status(client):
    resp = await client.get("/api/voice/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "gemini-voice"
    assert data["status"] == "active"
    assert "active_sessions" in data
    assert "max_sessions" in data


@pytest.mark.asyncio
async def test_voice_tools(client):
    resp = await client.get("/api/voice/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 6
    tool_names = [t["name"] for t in data["tools"]]
    assert "get_exceptions" in tool_names
    assert "get_reconciliation_status" in tool_names
    assert "approve_exception" in tool_names
    assert "get_audit_log" in tool_names
