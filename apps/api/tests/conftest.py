"""Shared test fixtures for LedgerLive API tests."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, AUDIT_LOG


@pytest.fixture(autouse=True)
def _clear_audit_log():
    """Clear audit log before each test."""
    AUDIT_LOG.clear()
    yield
    AUDIT_LOG.clear()


@pytest.fixture
async def client():
    """Async HTTP client for testing FastAPI endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
