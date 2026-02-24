"""Golden Scenario Truthfulness Tests — v0.301.1-ledgerlive

PROJECT_ID: LEDGERLIVE

Tests:
  1. Guard: 403 without DEMO+E2E
  2. Guard: 200/201 with DEMO+E2E
  3. Assertions computed from real state (not constants)
  4. actual_counts match expected_counts after full seed
  5. binder hashes present and stable two-run
  6. assertions_signature present and changes on tamper
  7. Tamper detection: modifying artifact changes signature
"""
import os
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app, AUDIT_LOG
from app.services.golden_scenario import service, GRC, EXPECTED_COUNTS, BASELINE_PATH


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def _reset_golden():
    """Reset golden state and audit log before/after each test."""
    service.reset()
    AUDIT_LOG.clear()
    yield
    service.reset()
    AUDIT_LOG.clear()


@pytest.fixture
async def demo_client(monkeypatch):
    """Async HTTP client with DEMO+E2E mode enabled."""
    monkeypatch.setenv("APP_MODE", "DEMO")
    monkeypatch.setenv("E2E_MODE", "1")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ── Guard Tests ───────────────────────────────────────────────────────

def test_require_e2e_mode_raises_without_env(monkeypatch):
    """require_e2e_mode() raises 403 when not in DEMO+E2E mode."""
    monkeypatch.setenv("APP_MODE", "LOCAL")
    monkeypatch.setenv("E2E_MODE", "0")
    from app.routers.golden_scenario import require_e2e_mode
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        require_e2e_mode()
    assert exc.value.status_code == 403
    assert "APP_MODE=DEMO" in exc.value.detail


def test_require_e2e_mode_passes_in_demo_e2e(monkeypatch):
    """require_e2e_mode() does not raise when APP_MODE=DEMO and E2E_MODE=1."""
    monkeypatch.setenv("APP_MODE", "DEMO")
    monkeypatch.setenv("E2E_MODE", "1")
    from app.routers.golden_scenario import require_e2e_mode
    # Should not raise
    require_e2e_mode()


def test_require_e2e_mode_raises_when_only_demo_no_e2e(monkeypatch):
    """APP_MODE=DEMO without E2E_MODE=1 is still blocked."""
    monkeypatch.setenv("APP_MODE", "DEMO")
    monkeypatch.setenv("E2E_MODE", "0")
    from app.routers.golden_scenario import require_e2e_mode
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        require_e2e_mode()
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_golden_endpoints_blocked_local_mode(monkeypatch):
    """Golden endpoints return 403 when APP_MODE=LOCAL (default)."""
    monkeypatch.setenv("APP_MODE", "LOCAL")
    monkeypatch.setenv("E2E_MODE", "0")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/ops/golden-scenario-run")
        assert r.status_code == 403


@pytest.mark.asyncio
async def test_golden_seed_accessible_in_demo_e2e(demo_client):
    """Seed endpoint returns 201 with expected structure in DEMO+E2E mode."""
    r = await demo_client.post("/api/ops/golden-scenario-run")
    assert r.status_code == 201
    data = r.json()
    assert data["seeded"] is True
    assert data["scenario"] == "golden_race_control"
    assert "ids" in data
    assert len(data["ids"]) == 18


# ── Truthfulness Tests ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_assertions_include_all_required_fields(demo_client):
    """get_assertions() returns all required truthfulness fields."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r = await demo_client.get("/api/ops/e2e-assertions")
    assert r.status_code == 200
    a = r.json()

    required_fields = [
        "scenario", "ids", "expected_counts", "actual_counts",
        "expected_binder_sha256", "actual_binder_sha256",
        "telemetry_pack", "court_pack", "replay",
        "security_event", "assertions_signature",
    ]
    for field in required_fields:
        assert field in a, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_actual_counts_match_expected_counts_after_seed(demo_client):
    """After seed, actual_counts must equal expected_counts exactly."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r = await demo_client.get("/api/ops/e2e-assertions")
    a = r.json()

    actual = a["actual_counts"]
    expected = a["expected_counts"]
    for key, exp_val in expected.items():
        assert actual.get(key) == exp_val, (
            f"actual_counts[{key!r}]={actual.get(key)!r}, expected {exp_val!r}"
        )


@pytest.mark.asyncio
async def test_binder_hash_is_real_sha256(demo_client):
    """actual_binder_sha256 is a real sha256 hex string, not a placeholder."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r = await demo_client.get("/api/ops/e2e-assertions")
    a = r.json()

    actual_h = a["actual_binder_sha256"]
    assert actual_h.startswith("sha256:"), f"Expected sha256: prefix, got {actual_h!r}"
    hex_part = actual_h.replace("sha256:", "")
    assert len(hex_part) == 64, f"Expected 64-char hex, got {len(hex_part)} chars"
    # Must NOT be the old placeholder
    assert "deadbeef" not in hex_part, "Binder hash still uses placeholder!"


@pytest.mark.asyncio
async def test_assertions_signature_is_real_sha256(demo_client):
    """assertions_signature is a real sha256 hex string."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r = await demo_client.get("/api/ops/e2e-assertions")
    a = r.json()

    sig = a["assertions_signature"]
    assert sig.startswith("sha256:")
    assert len(sig) == 71  # 7 ("sha256:") + 64 (hex)


@pytest.mark.asyncio
async def test_telemetry_pack_has_sha256_and_pass(demo_client):
    """Telemetry pack has status=PASS and a real sha256."""
    await demo_client.post("/api/ops/golden-scenario-run")
    # Export is done automatically on seed; also call explicitly to confirm
    await demo_client.post("/api/ops/export/telemetry-pack")
    r = await demo_client.get("/api/ops/e2e-assertions")
    a = r.json()

    tp = a["telemetry_pack"]
    assert tp["status"] == "PASS"
    assert tp["sha256"].startswith("sha256:")
    assert "deadbeef" not in tp["sha256"], "Telemetry pack still uses placeholder hash!"


@pytest.mark.asyncio
async def test_court_pack_has_sha256_and_pass(demo_client):
    """Court pack has status=PASS and a real sha256."""
    await demo_client.post("/api/ops/golden-scenario-run")
    await demo_client.post("/api/ops/export/court-pack")
    r = await demo_client.get("/api/ops/e2e-assertions")
    a = r.json()

    cp = a["court_pack"]
    assert cp["status"] == "PASS"
    assert cp["sha256"].startswith("sha256:")
    assert "deadbeef" not in cp["sha256"], "Court pack still uses placeholder hash!"


@pytest.mark.asyncio
async def test_replay_matches_original_after_regen(demo_client):
    """After regenerate-binder, replay.matches_original is True."""
    await demo_client.post("/api/ops/golden-scenario-run")
    # Update baseline to current hash so matches_original = True
    await demo_client.post("/api/ops/update-baseline")
    await demo_client.post("/api/ops/replay/regenerate-binder")

    r = await demo_client.get("/api/ops/e2e-assertions")
    a = r.json()

    replay = a["replay"]
    assert replay["matches_original"] is True, (
        f"replay.matches_original={replay['matches_original']!r}. "
        f"regen={replay.get('regen_binder_sha256')!r}, "
        f"expected={a.get('expected_binder_sha256')!r}"
    )
    assert replay["status"] == "PASS"
    assert replay["regen_binder_sha256"].startswith("sha256:")


@pytest.mark.asyncio
async def test_assertions_signature_stable_across_two_calls(demo_client):
    """Calling get_assertions() twice without changes returns identical signatures."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r1 = await demo_client.get("/api/ops/e2e-assertions")
    r2 = await demo_client.get("/api/ops/e2e-assertions")
    assert r1.json()["assertions_signature"] == r2.json()["assertions_signature"]


# ── Tamper Detection Tests ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_tamper_changes_assertions_signature(demo_client):
    """Tampering an artifact changes assertions_signature (proves truthfulness)."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r1 = await demo_client.get("/api/ops/e2e-assertions")
    sig1 = r1.json()["assertions_signature"]

    # Tamper: force telemetry pack status to TAMPERED
    tr = await demo_client.post("/api/ops/tamper-artifact", json={
        "artifact_key": "telemetry_pack",
        "field": "status",
        "value": "TAMPERED",
    })
    assert tr.status_code == 200
    assert tr.json()["tampered"] is True

    r2 = await demo_client.get("/api/ops/e2e-assertions")
    sig2 = r2.json()["assertions_signature"]
    a2 = r2.json()

    assert sig1 != sig2, "Signature MUST change after tampering artifact!"
    assert a2["telemetry_pack"]["status"] == "TAMPERED"


@pytest.mark.asyncio
async def test_tamper_hash_changes_assertions_signature(demo_client):
    """Tampering pack hash changes assertions_signature."""
    await demo_client.post("/api/ops/golden-scenario-run")
    r1 = await demo_client.get("/api/ops/e2e-assertions")
    sig1 = r1.json()["assertions_signature"]

    # Tamper: inject a fake hash for court_pack
    await demo_client.post("/api/ops/tamper-artifact", json={
        "artifact_key": "court_pack",
        "field": "hash",
        "value": "sha256:aaaa1111" + "0" * 56,
    })

    r2 = await demo_client.get("/api/ops/e2e-assertions")
    sig2 = r2.json()["assertions_signature"]

    assert sig1 != sig2, "Signature MUST change after tampering court_pack hash!"


# ── Service-level Tests (no HTTP) ─────────────────────────────────────

def test_service_compute_actual_counts_empty():
    """Before seeding, actual_counts returns zeros."""
    counts = service._compute_actual_counts()
    assert counts["lanes"] == 0
    assert counts["checkpoints"] == 0
    assert counts["exceptions"] == 0


def test_service_binder_hash_after_seed():
    """Binder hash is a real sha256 after seeding."""
    service.seed()
    h = service._compute_binder_hash()
    assert h.startswith("sha256:")
    assert len(h) == 71
    assert "deadbeef" not in h


def test_service_binder_hash_stable_two_seeds():
    """Binder hash is stable across two consecutive seeds (deterministic)."""
    service.seed()
    h1 = service._compute_binder_hash()
    service.seed()
    h2 = service._compute_binder_hash()
    assert h1 == h2, f"Binder hash differs across seeds: {h1!r} vs {h2!r}"


def test_service_assertions_signature_changes_on_tamper():
    """Service tamper_artifact() causes get_assertions() signature to change."""
    service.seed()
    a1 = service.get_assertions()
    sig1 = a1["assertions_signature"]

    service.tamper_artifact("telemetry_pack", "status", "INJECTED")
    a2 = service.get_assertions()
    sig2 = a2["assertions_signature"]

    assert sig1 != sig2, "signatures must differ after tamper"
    assert a2["telemetry_pack"]["status"] == "INJECTED"


def test_service_update_baseline_writes_file(tmp_path, monkeypatch):
    """write_baseline_binder_hash() creates baseline file with real sha256."""
    import app.services.golden_scenario as gs_mod
    original_path = gs_mod.BASELINE_PATH
    test_baseline = tmp_path / "golden_binder_sha256.txt"
    monkeypatch.setattr(gs_mod, "BASELINE_PATH", test_baseline)

    service.seed()
    written = service.write_baseline_binder_hash()
    assert test_baseline.read_text().strip() == written
    assert written.startswith("sha256:")
    assert "deadbeef" not in written

    # Restore
    monkeypatch.setattr(gs_mod, "BASELINE_PATH", original_path)


def test_service_audit_events_on_seed():
    """seed() emits audit events for each seeded artifact category."""
    service.seed()
    event_types = {e["action"] for e in AUDIT_LOG}
    assert "grc_seed_lane" in event_types
    assert "grc_seed_checkpoint" in event_types
    assert "grc_seed_incident" in event_types
    assert "grc_seed_approval" in event_types
    assert "grc_security_block" in event_types
    assert "grc_seed_exception" in event_types
