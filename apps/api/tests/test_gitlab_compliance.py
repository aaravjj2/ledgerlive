"""Tests for GitLab Compliance Agent."""
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


SAMPLE_DIFF_HIGH = """-tolerance: 0.01
+tolerance: 0.05
"""

SAMPLE_DIFF_CRITICAL = """-exception_flag: true
+exception_flag: false
"""

SAMPLE_DIFF_CLEAN = """+description: Updated vendor name
-description: Old vendor name
"""


@pytest.mark.asyncio
async def test_compliance_check_high_risk(client):
    resp = await client.post("/api/gitlab/compliance-check", json={
        "diff": SAMPLE_DIFF_HIGH,
        "file_path": "config/reconciliation_rules.yaml",
        "mr_url": "https://gitlab.com/test/mr/1",
        "author": "dev1",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_findings"] >= 1
    assert data["requires_cfo_approval"] is True


@pytest.mark.asyncio
async def test_compliance_check_critical(client):
    resp = await client.post("/api/gitlab/compliance-check", json={
        "diff": SAMPLE_DIFF_CRITICAL,
        "file_path": "config/thresholds.yaml",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["critical_count"] >= 1
    assert data["requires_cfo_approval"] is True


@pytest.mark.asyncio
async def test_compliance_check_clean(client):
    resp = await client.post("/api/gitlab/compliance-check", json={
        "diff": SAMPLE_DIFF_CLEAN,
        "file_path": "config/vendors.yaml",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_findings"] == 0
    assert data["requires_cfo_approval"] is False


@pytest.mark.asyncio
async def test_audit_artifact(client):
    resp = await client.post("/api/gitlab/audit-artifact", json={
        "mr_url": "https://gitlab.com/test/mr/1",
        "author": "dev1",
        "changed_files": ["config/thresholds.yaml"],
        "findings_summary": "1 CRITICAL finding: exception flag disabled",
        "approver": "cfo@company.com",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "sha256" in data
    assert len(data["sha256"]) == 64
    assert "artifact" in data


@pytest.mark.asyncio
async def test_compliance_rules_list(client):
    resp = await client.get("/api/gitlab/compliance-rules")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 10


@pytest.mark.asyncio
async def test_green_agent_stats(client):
    resp = await client.get("/api/gitlab/green-agent-stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["carbon_aware"] is True
    assert "tiers" in data
