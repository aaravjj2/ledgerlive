"""test_airia_compat.py — Airia Compatibility Report determinism + tamper assertions.

Tests:
- Running compat report twice yields byte-identical output
- All checks produce PASS for the committed bundle
- Tamper check: modifying a bundle file makes checksums FAIL
- Report shape is correct
- API endpoint returns 200 with overall PASS

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import copy
import json
import tempfile
import shutil
from pathlib import Path

import pytest

from app.services.airia_compat import (
    run_compat_report,
    _check_bundle_structure,
    _check_workflow_dag,
    _check_fail_closed,
    _check_approvals_present,
    _check_checksums,
    _canonical_json,
    _sha256,
    BUNDLE_DIR,
)

# ── Basic shape ───────────────────────────────────────────────────────────────

def test_compat_report_shape():
    report = run_compat_report()
    assert "overall" in report
    assert "checks" in report
    assert "bundle_sha256" in report
    assert "blueprint_sha256" in report
    assert "tools_sha256" in report
    assert "report_signature_sha256" in report
    assert "pass_count" in report
    assert "fail_count" in report


def test_compat_report_checks_count():
    report = run_compat_report()
    assert len(report["checks"]) == 10, "Must have exactly 10 checks (7 bundle + 3 MCP)"


def test_compat_report_overall_pass():
    report = run_compat_report()
    assert report["overall"] == "PASS", (
        f"Compat report must be PASS. Failing checks: "
        f"{[c for c in report['checks'] if not c['passed']]}"
    )


def test_compat_report_all_checks_pass():
    report = run_compat_report()
    for check in report["checks"]:
        assert check["passed"], (
            f"Check {check['id']} should PASS but got FAIL: {check['reason']}"
        )
        assert check["status"] == "PASS"


# ── Each check has required fields ───────────────────────────────────────────

def test_compat_check_fields():
    report = run_compat_report()
    for check in report["checks"]:
        assert "id" in check, f"Check missing 'id': {check}"
        assert "name" in check, f"Check missing 'name': {check}"
        assert "passed" in check, f"Check missing 'passed': {check}"
        assert "status" in check, f"Check missing 'status': {check}"
        assert "reason" in check, f"Check missing 'reason': {check}"


# ── Determinism ──────────────────────────────────────────────────────────────

def test_compat_report_deterministic():
    """Running run_compat_report() twice must yield byte-identical canonical JSON."""
    r1 = run_compat_report()
    r2 = run_compat_report()
    assert r1 == r2, "Compat report must be identical on two runs"

    b1 = _canonical_json(r1)
    b2 = _canonical_json(r2)
    assert b1 == b2, "Canonical JSON must be byte-identical across two runs"


def test_compat_report_signature_stable():
    r1 = run_compat_report()
    r2 = run_compat_report()
    assert r1["report_signature_sha256"] == r2["report_signature_sha256"], (
        "Report signature sha256 must be stable across runs"
    )


# ── Tamper detection ─────────────────────────────────────────────────────────

def test_tamper_checksums_fails():
    """Tamper a bundle file → checksums check must return FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        # Copy bundle to temp dir
        shutil.copytree(str(BUNDLE_DIR), str(tmp_dir / "bundle"))
        tampered_dir = tmp_dir / "bundle"

        # Tamper: append garbage to manifest.json
        manifest_path = tampered_dir / "manifest.json"
        original = manifest_path.read_bytes()
        manifest_path.write_bytes(original + b"\n// tampered")

        # Regenerate checksums.txt to still have the old hash → mismatch
        result = _check_checksums(tampered_dir)
        assert result["status"] == "FAIL", (
            "Tampered bundle must cause checksums check to FAIL"
        )
        assert not result["passed"]


def test_tamper_structure_fails():
    """Remove a required file → bundle structure check must FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        shutil.copytree(str(BUNDLE_DIR), str(tmp_dir / "bundle"))
        tampered_dir = tmp_dir / "bundle"

        # Remove verify_bundle.py
        (tampered_dir / "verify_bundle.py").unlink()

        result = _check_bundle_structure(tampered_dir)
        assert result["status"] == "FAIL"
        assert not result["passed"]
        assert "verify_bundle.py" in result["reason"]


# ── Individual check functions work independently ─────────────────────────────

def test_workflow_dag_check_pass():
    result = _check_workflow_dag(BUNDLE_DIR)
    assert result["passed"], f"DAG check failed: {result['reason']}"


def test_fail_closed_check_pass():
    result = _check_fail_closed(BUNDLE_DIR)
    assert result["passed"], f"Fail-closed check failed: {result['reason']}"


def test_approvals_check_pass():
    result = _check_approvals_present(BUNDLE_DIR)
    assert result["passed"], f"Approvals check failed: {result['reason']}"


# ── SHA256 fields are real hashes ────────────────────────────────────────────

def test_bundle_sha256_is_real():
    report = run_compat_report()
    sha = report["bundle_sha256"]
    assert sha != "missing", "bundle_sha256 must not be 'missing'"
    assert len(sha) == 64, f"bundle_sha256 must be 64 hex chars, got: {sha!r}"


def test_blueprint_sha256_is_real():
    report = run_compat_report()
    sha = report["blueprint_sha256"]
    assert sha != "missing"
    assert len(sha) == 64


def test_tools_sha256_is_real():
    report = run_compat_report()
    sha = report["tools_sha256"]
    assert sha != "missing"
    assert len(sha) == 64


def test_signature_sha256_is_real():
    report = run_compat_report()
    sha = report["report_signature_sha256"]
    assert len(sha) == 64


# ── pass_count + fail_count consistent ───────────────────────────────────────

def test_pass_fail_counts():
    report = run_compat_report()
    checks = report["checks"]
    expected_pass = sum(1 for c in checks if c["passed"])
    expected_fail = sum(1 for c in checks if not c["passed"])
    assert report["pass_count"] == expected_pass
    assert report["fail_count"] == expected_fail
    assert report["pass_count"] + report["fail_count"] == len(checks)


# ── MCP checks (new in iteration 1) ──────────────────────────────────────────

def test_compat_report_now_has_10_checks():
    report = run_compat_report()
    assert len(report["checks"]) == 10, (
        f"Expected 10 checks after MCP additions, got {len(report['checks'])}"
    )


def test_compat_mcp_server_present_passes():
    from app.services.airia_compat import _check_mcp_server_present
    result = _check_mcp_server_present()
    assert result["passed"] is True, f"mcp_server_present should PASS: {result['reason']}"


def test_compat_mcp_tools_match_registry_passes():
    from app.services.airia_compat import _check_mcp_tools_match_registry
    result = _check_mcp_tools_match_registry()
    assert result["passed"] is True, f"mcp_tools_match_registry should PASS: {result['reason']}"


def test_compat_mcp_config_generated_passes():
    from app.services.airia_compat import _check_mcp_config_generated
    result = _check_mcp_config_generated()
    assert result["passed"] is True, f"mcp_config_generated should PASS: {result['reason']}"


def test_compat_mcp_check_ids_present():
    report = run_compat_report()
    ids = [c["id"] for c in report["checks"]]
    assert "mcp_server_present" in ids
    assert "mcp_tools_match_registry" in ids
    assert "mcp_config_generated" in ids


def test_compat_mcp_config_determinism():
    """Two calls return same config SHA-256."""
    from app.services.mcp_server import generate_airia_config
    c1 = generate_airia_config()
    c2 = generate_airia_config()
    assert c1["config_sha256"] == c2["config_sha256"]
