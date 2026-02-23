"""Tests for health endpoint and core configuration."""
import pytest


@pytest.mark.asyncio
async def test_healthz_returns_ok(client):
    r = await client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["project"] == "LEDGERLIVE"
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_healthz_contains_mode(client):
    r = await client.get("/healthz")
    data = r.json()
    assert "mode" in data
    assert "llm" in data
    assert "ts" in data


@pytest.mark.asyncio
async def test_audit_log_empty_initially(client):
    r = await client.get("/api/audit")
    assert r.status_code == 200
    data = r.json()
    assert data["events"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_project_id_file():
    """PROJECT_ID file must contain LEDGERLIVE."""
    import pathlib
    pid = pathlib.Path(__file__).resolve().parents[3] / "PROJECT_ID"
    assert pid.read_text().strip() == "LEDGERLIVE"
