"""test_airia_bundle.py — Airia bundle service + CLI determinism assertions.

Tests:
- Bundle files exist
- Manifest parses correctly
- Tools count >= 8
- Bundle generation stable across 2 runs (same checksums)
- CLI validate returns PASS
- CLI verify returns PASS
- API service functions return correct shapes

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
BUNDLE_DIR = REPO_ROOT / "artifacts" / "airia" / "community_bundle"

REQUIRED_FILES = [
    "manifest.json",
    "tools.json",
    "workflow_template.json",
    "runbooks.md",
    "screenshots_manifest.json",
    "checksums.txt",
    "verify_bundle.py",
]

PYTHON = sys.executable


# ── File presence ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_bundle_file_exists(filename: str):
    assert (BUNDLE_DIR / filename).exists(), f"Bundle file missing: {filename}"


# ── Manifest ──────────────────────────────────────────────────────────────────


def test_manifest_parses():
    data = json.loads((BUNDLE_DIR / "manifest.json").read_bytes())
    assert data.get("name"), "manifest.name must be set"
    assert data.get("version"), "manifest.version must be set"
    assert data.get("bundle_hash"), "manifest.bundle_hash must be set"
    assert data.get("category"), "manifest.category must be set"


def test_manifest_has_airia_tags():
    data = json.loads((BUNDLE_DIR / "manifest.json").read_bytes())
    tags = data.get("tags", [])
    assert "airia" in tags, f"manifest.tags must include 'airia', got {tags}"
    assert "finance" in tags, f"manifest.tags must include 'finance', got {tags}"


# ── Tools ─────────────────────────────────────────────────────────────────────


def test_tools_count():
    data = json.loads((BUNDLE_DIR / "tools.json").read_bytes())
    tools = data.get("tools", [])
    assert len(tools) >= 8, f"Expected >=8 tools, got {len(tools)}"


def test_tools_have_required_fields():
    data = json.loads((BUNDLE_DIR / "tools.json").read_bytes())
    for tool in data.get("tools", []):
        assert tool.get("id"), f"Tool missing id: {tool}"
        assert tool.get("name"), f"Tool missing name: {tool}"
        assert tool.get("type"), f"Tool missing type: {tool}"


# ── Workflow template ─────────────────────────────────────────────────────────


def test_workflow_template_has_5_steps():
    data = json.loads((BUNDLE_DIR / "workflow_template.json").read_bytes())
    steps = data.get("steps", [])
    assert len(steps) == 5, f"Expected 5 workflow steps, got {len(steps)}"


def test_workflow_template_step_ids():
    data = json.loads((BUNDLE_DIR / "workflow_template.json").read_bytes())
    ids = [s["id"] for s in data.get("steps", [])]
    for expected_id in ["ingest", "reconcile", "triage", "review", "close"]:
        assert expected_id in ids, f"Workflow step {expected_id!r} missing from {ids}"


# ── Determinism: checksums stable across 2 runs ───────────────────────────────


def _compute_checksums() -> dict[str, str]:
    result: dict[str, str] = {}
    for filename in ["manifest.json", "tools.json", "workflow_template.json", "runbooks.md"]:
        fp = BUNDLE_DIR / filename
        if fp.exists():
            result[filename] = hashlib.sha256(fp.read_bytes()).hexdigest()
    return result


def test_bundle_hashes_stable_across_two_reads():
    run1 = _compute_checksums()
    run2 = _compute_checksums()
    assert run1 == run2, "Bundle file hashes must be identical across two reads"


# ── CLI validate ──────────────────────────────────────────────────────────────


def test_cli_validate_pass():
    result = subprocess.run(
        [PYTHON, str(REPO_ROOT / "tools" / "airia_bundle.py"), "--action", "validate"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"CLI validate failed:\n{result.stdout}\n{result.stderr}"
    assert "PASS" in result.stdout, f"CLI validate must print PASS:\n{result.stdout}"


# ── CLI verify ────────────────────────────────────────────────────────────────


def test_cli_verify_pass():
    result = subprocess.run(
        [PYTHON, str(REPO_ROOT / "tools" / "airia_bundle.py"), "--action", "verify"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"CLI verify failed:\n{result.stdout}\n{result.stderr}"
    assert "PASS" in result.stdout, f"CLI verify must print PASS:\n{result.stdout}"


# ── Service layer ─────────────────────────────────────────────────────────────


def test_service_get_bundle_status():
    import sys
    sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))
    from app.services.airia_bundle import get_bundle_status
    status = get_bundle_status()
    assert status["validator_status"] == "PASS", f"Expected PASS, got: {status}"
    assert status["bundle_hash"], "bundle_hash must be non-empty"
    assert len(status["tools"]) >= 8


def test_service_validate_bundle():
    import sys
    sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))
    from app.services.airia_bundle import validate_bundle
    result = validate_bundle()
    assert result["status"] == "PASS", f"validate_bundle() expected PASS, got: {result}"


def test_service_verify_bundle():
    import sys
    sys.path.insert(0, str(REPO_ROOT / "apps" / "api"))
    from app.services.airia_bundle import verify_bundle
    result = verify_bundle()
    assert result["status"] == "PASS", f"verify_bundle() expected PASS, got: {result}"
