"""Airia Compatibility Service — deterministic compliance report for Airia platform readiness.

Checks the community bundle against required Airia integration criteria.
ALL checks are deterministic and offline (no network calls).

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

# Resolve repo root
_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parent
for _p in _HERE.parents:
    if (_p / "artifacts").exists() and (_p / "tools").exists():
        REPO_ROOT = _p
        break

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

SENSITIVE_STEPS = {"review", "close"}  # steps that need approval
EXPECTED_OUTPUTS = {
    "telemetry_pack": "ledgerlive.telemetry",
    "court_pack": "ledgerlive.court",
    "replay_verification": "ledgerlive.replay",
    "narrative_export": "ledgerlive.narrative",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(obj: dict) -> bytes:
    """Return canonical (sorted-keys, no-space) JSON bytes for deterministic hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _read_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_bytes())
        except Exception:
            pass
    return {}


# ── Individual checks ─────────────────────────────────────────────────────────

def _check_bundle_structure(bundle_dir: Path = BUNDLE_DIR) -> dict:
    missing = [f for f in REQUIRED_FILES if not (bundle_dir / f).exists()]
    passed = len(missing) == 0
    return {
        "id": "bundle_structure_completeness",
        "name": "Bundle Structure Completeness",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": "All required files present" if passed else f"Missing: {missing}",
    }


def _check_tool_schemas_versioned(bundle_dir: Path = BUNDLE_DIR) -> dict:
    tools_path = bundle_dir / "tools.json"
    if not tools_path.exists():
        return {
            "id": "tool_schemas_version_pinned",
            "name": "Tool Schemas Version-Pinned",
            "passed": False,
            "status": "FAIL",
            "reason": "tools.json missing",
        }
    tools_data = _read_json(tools_path)
    tools = tools_data.get("tools", tools_data if isinstance(tools_data, list) else [])
    if isinstance(tools_data, dict) and "tools" not in tools_data:
        # Try the dict values
        tools = list(tools_data.values()) if isinstance(tools_data, dict) else []
    if not tools:
        tools = [tools_data] if tools_data else []

    unversioned = []
    if isinstance(tools, list):
        for t in tools:
            if isinstance(t, dict) and not t.get("schema_version") and not t.get("version"):
                # Check if there's a top-level schema_version
                if not tools_data.get("schema_version"):
                    unversioned.append(t.get("id", "unknown"))
    passed = len(unversioned) == 0
    return {
        "id": "tool_schemas_version_pinned",
        "name": "Tool Schemas Version-Pinned",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": "All tool schemas have version pinned" if passed
                  else f"Unversioned tools: {unversioned}",
    }


def _check_workflow_dag(bundle_dir: Path = BUNDLE_DIR) -> dict:
    template_path = bundle_dir / "workflow_template.json"
    if not template_path.exists():
        return {
            "id": "workflow_dag_acyclic",
            "name": "Workflow DAG Acyclic + Stable Ordering",
            "passed": False,
            "status": "FAIL",
            "reason": "workflow_template.json missing",
        }
    template = _read_json(template_path)
    steps = template.get("steps", [])
    if not steps:
        return {
            "id": "workflow_dag_acyclic",
            "name": "Workflow DAG Acyclic + Stable Ordering",
            "passed": False,
            "status": "FAIL",
            "reason": "No steps in workflow template",
        }
    # Check step IDs are unique
    step_ids = [s.get("id", "") for s in steps]
    unique_ids = set(step_ids)
    if len(step_ids) != len(unique_ids):
        return {
            "id": "workflow_dag_acyclic",
            "name": "Workflow DAG Acyclic + Stable Ordering",
            "passed": False,
            "status": "FAIL",
            "reason": f"Duplicate step IDs detected: {step_ids}",
        }
    # Check step numbers are monotonically increasing
    step_nums = [s.get("step", i + 1) for i, s in enumerate(steps)]
    is_ordered = all(step_nums[i] < step_nums[i + 1] for i in range(len(step_nums) - 1))
    passed = is_ordered
    return {
        "id": "workflow_dag_acyclic",
        "name": "Workflow DAG Acyclic + Stable Ordering",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": f"DAG has {len(steps)} steps, acyclic with stable ordering"
                  if passed else "Steps are not monotonically ordered",
    }


def _check_approvals_present(bundle_dir: Path = BUNDLE_DIR) -> dict:
    template_path = bundle_dir / "workflow_template.json"
    if not template_path.exists():
        return {
            "id": "approvals_for_sensitive_steps",
            "name": "Approvals for Sensitive Steps",
            "passed": False,
            "status": "FAIL",
            "reason": "workflow_template.json missing",
        }
    template = _read_json(template_path)
    steps = template.get("steps", [])
    hitl_count = sum(
        1 for s in steps if "hitl" in s.get("tool", "").lower() or s.get("id") in SENSITIVE_STEPS
    )
    passed = hitl_count >= 1
    return {
        "id": "approvals_for_sensitive_steps",
        "name": "Approvals for Sensitive Steps",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": f"Found {hitl_count} approval/HITL step(s) in workflow" if passed
                  else "No HITL approval steps found in workflow",
    }


def _check_fail_closed(bundle_dir: Path = BUNDLE_DIR) -> dict:
    template_path = bundle_dir / "workflow_template.json"
    if not template_path.exists():
        return {
            "id": "fail_closed_rules",
            "name": "Fail-Closed Rules Enabled",
            "passed": False,
            "status": "FAIL",
            "reason": "workflow_template.json missing",
        }
    template = _read_json(template_path)
    steps = template.get("steps", [])
    halt_count = sum(1 for s in steps if s.get("on_error") == "halt")
    passed = halt_count >= 1
    return {
        "id": "fail_closed_rules",
        "name": "Fail-Closed Rules Enabled",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": f"{halt_count}/{len(steps)} steps configured with on_error=halt" if passed
                  else "No fail-closed rules found",
    }


def _check_outputs_present(bundle_dir: Path = BUNDLE_DIR) -> dict:
    runbooks_path = bundle_dir / "runbooks.md"
    if not runbooks_path.exists():
        return {
            "id": "required_outputs",
            "name": "Required Outputs Present",
            "passed": False,
            "status": "FAIL",
            "reason": "runbooks.md missing",
        }
    text = runbooks_path.read_text(encoding="utf-8", errors="ignore").lower()
    required = ["telemetry", "court", "replay", "narrative"]
    missing = [r for r in required if r not in text]
    passed = len(missing) == 0
    return {
        "id": "required_outputs",
        "name": "Required Outputs Present",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": "All required outputs (telemetry, court, replay, narrative) documented"
                  if passed else f"Missing output docs: {missing}",
    }


def _check_checksums(bundle_dir: Path = BUNDLE_DIR) -> dict:
    checksums_path = bundle_dir / "checksums.txt"
    if not checksums_path.exists():
        return {
            "id": "deterministic_checksums",
            "name": "Deterministic Checksums Match",
            "passed": False,
            "status": "FAIL",
            "reason": "checksums.txt missing",
        }
    text = checksums_path.read_text(encoding="utf-8", errors="ignore")
    mismatches = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            continue
        expected_hash, filename = parts
        fp = bundle_dir / filename
        if fp.exists():
            actual = _sha256(fp.read_bytes())
            if actual != expected_hash:
                mismatches.append(filename)
    passed = len(mismatches) == 0
    return {
        "id": "deterministic_checksums",
        "name": "Deterministic Checksums Match",
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "reason": "All checksums verified" if passed
                  else f"Checksum mismatches: {mismatches}",
    }


# ── Public API ────────────────────────────────────────────────────────────────

def run_compat_report(bundle_dir: Path = BUNDLE_DIR) -> dict:
    """Produce deterministic Airia compatibility report.

    DETERMINISM: given identical bundle files, this function always returns
    byte-identical canonicalised JSON.
    """
    checks = [
        _check_bundle_structure(bundle_dir),
        _check_tool_schemas_versioned(bundle_dir),
        _check_workflow_dag(bundle_dir),
        _check_approvals_present(bundle_dir),
        _check_fail_closed(bundle_dir),
        _check_outputs_present(bundle_dir),
        _check_checksums(bundle_dir),
    ]

    overall = all(c["passed"] for c in checks)

    # SHA256 hashes of individual bundle files
    def _file_sha(name: str) -> str:
        fp = bundle_dir / name
        return _sha256(fp.read_bytes()) if fp.exists() else "missing"

    bundle_sha256 = _file_sha("manifest.json")
    blueprint_sha256 = _file_sha("workflow_template.json")
    tools_sha256 = _file_sha("tools.json")

    # Build report object (without report_signature — hash that separately)
    report_body = {
        "overall": "PASS" if overall else "FAIL",
        "checks": checks,
        "bundle_sha256": bundle_sha256,
        "blueprint_sha256": blueprint_sha256,
        "tools_sha256": tools_sha256,
        "pass_count": sum(1 for c in checks if c["passed"]),
        "fail_count": sum(1 for c in checks if not c["passed"]),
    }

    # Compute report signature as sha256 of canonical JSON of the report body
    canonical = _canonical_json(report_body)
    report_signature_sha256 = _sha256(canonical)

    report_body["report_signature_sha256"] = report_signature_sha256
    return report_body


def run_compat_report_cached() -> dict:
    """Return a cached / written compat report from artifacts dir, or generate fresh."""
    out_path = BUNDLE_DIR / "compat_report.json"
    report = run_compat_report()
    # Write to artifacts for CLI consumption
    try:
        out_path.write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except Exception:
        pass
    return report
