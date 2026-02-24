#!/usr/bin/env python3
"""
Apex Terminal — Proof Pack Validator
======================================
Checks a proof pack directory for constitution compliance.

Usage:
    py tools/proof/validate_proof_pack.py <proof-pack-dir>

Exit codes:
    0  – all checks pass
    1  – one or more checks fail
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_FILES = [
    "MANIFEST.md",
    "manifest.json",
    "README.md",
    "no-demo-gate-output.txt",
    "tsc-output.txt",
    "meta-guards-output.txt",
    "pytest-output.txt",
    "playwright-output.txt",
]

REQUIRED_DIRS = [
    "playwright-report",
    "test-results",
    "screenshots",
]

REQUIRED_GATES = ["no-demo-gate", "tsc", "meta-guards", "pytest", "playwright"]

# Minimum TOUR video size in bytes (180 s × ~8 KB/s WebM ≈ 1.44 MB)
TOUR_MIN_BYTES = 1_000_000


def check(cond: bool, label: str, detail: str = "") -> bool:
    icon = "✅" if cond else "❌"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {icon} {label}{suffix}")
    return cond


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: py tools/proof/validate_proof_pack.py <proof-pack-dir>")
        return 2

    pack_dir = Path(sys.argv[1])
    if not pack_dir.is_dir():
        print(f"❌  Directory not found: {pack_dir}")
        return 1

    print(f"\n=== Proof Pack Validator ===")
    print(f"Directory: {pack_dir}\n")

    failures = 0

    # 1. Required flat files
    print("── Required files ──")
    for fname in REQUIRED_FILES:
        ok = check((pack_dir / fname).is_file(), fname)
        if not ok:
            failures += 1

    print()

    # 2. Required directories
    print("── Required directories ──")
    for dname in REQUIRED_DIRS:
        ok = check((pack_dir / dname).is_dir(), dname)
        if not ok:
            failures += 1

    print()

    # 3. TOUR.webm
    print("── TOUR.webm ──")
    tour = pack_dir / "TOUR.webm"
    if tour.is_file():
        size = tour.stat().st_size
        ok = check(size >= TOUR_MIN_BYTES, "TOUR.webm", f"{size/1_048_576:.1f} MB")
        if not ok:
            failures += 1
    else:
        print("  ⚠  TOUR.webm absent (required if UX changed)")
        failures += 1

    print()

    # 4. manifest.json structure + gate results
    print("── manifest.json ──")
    manifest_path = pack_dir / "manifest.json"
    if not manifest_path.is_file():
        print("  ❌  manifest.json missing — skipping gate checks")
        failures += 1
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"  ❌  manifest.json is not valid JSON: {exc}")
            failures += 1
            manifest = {}

        # schema_version
        ok = check(manifest.get("schema_version") == 1, "schema_version == 1")
        if not ok:
            failures += 1

        # overall
        overall = manifest.get("overall", "FAIL")
        ok = check(overall == "PASS", f"overall == PASS", f"got '{overall}'")
        if not ok:
            failures += 1

        # git_sha non-empty
        sha = manifest.get("git_sha", "")
        ok = check(bool(sha) and sha != "unknown", "git_sha present", sha)
        if not ok:
            failures += 1

        # each gate passed
        gates = manifest.get("gates", {})
        for gate in REQUIRED_GATES:
            gate_info = gates.get(gate, {})
            gate_passed = gate_info.get("passed", False)
            ok = check(gate_passed, f"gate '{gate}' passed",
                       f"exit={gate_info.get('returncode','?')}")
            if not ok:
                failures += 1

        # test counts — zero failures, zero skips
        test_counts = manifest.get("test_counts", {})
        for suite in ("pytest", "meta-guards", "playwright"):
            counts = test_counts.get(suite, {})
            failed  = counts.get("failed", 0)
            skipped = counts.get("skipped", 0)
            passed  = counts.get("passed", 0)
            ok_fail = check(failed  == 0, f"{suite}: 0 failed",  f"got {failed}")
            ok_skip = check(skipped == 0, f"{suite}: 0 skipped", f"got {skipped}")
            ok_pass = check(passed  >  0, f"{suite}: >0 passed", f"got {passed}")
            if not (ok_fail and ok_skip and ok_pass):
                failures += 1

    print()

    # 5. Selector lint — no forbidden selectors in E2E specs
    print("── E2E selector lint ──")
    e2e_dir = pack_dir.parent.parent.parent / "apps" / "web" / "e2e"
    if not e2e_dir.exists():
        # try relative to CWD
        import os
        e2e_dir = Path(os.getcwd()) / "apps" / "web" / "e2e"

    forbidden_patterns = [
        ".locator('.",
        '.locator(".',
        'getByRole(',
        'getByText(',
        'getByLabel(',
        'xpath=',
        'css=',
        '>>',
    ]
    forbidden_found: list[str] = []
    if e2e_dir.is_dir():
        for spec in e2e_dir.rglob("*.ts"):
            lines = spec.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # allow comments
                if stripped.startswith("//"):
                    continue
                for pat in forbidden_patterns:
                    if pat in line:
                        forbidden_found.append(f"{spec.name}:{i}: {stripped[:80]}")
    if forbidden_found:
        print(f"  ❌  Forbidden selectors found ({len(forbidden_found)}):")
        for item in forbidden_found[:10]:
            print(f"       {item}")
        failures += 1
    else:
        check(True, "No forbidden selectors (data-testid only)")

    print()

    # ── Summary ────────────────────────────────────────────────────────────
    if failures == 0:
        print("=" * 50)
        print("✅  PROOF PACK: VALID")
        print("=" * 50)
        return 0
    else:
        print("=" * 50)
        print(f"❌  PROOF PACK: INVALID  ({failures} check(s) failed)")
        print("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
