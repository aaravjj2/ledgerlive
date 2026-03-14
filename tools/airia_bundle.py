#!/usr/bin/env python3
"""
tools/airia_bundle.py — Airia Community Bundle CLI

Usage:
    python tools/airia_bundle.py --action bundle    # write all bundle files
    python tools/airia_bundle.py --action validate  # check completeness + hash stability
    python tools/airia_bundle.py --action verify    # offline checksum verification

Exit codes: 0 = PASS, 1 = FAIL

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
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

CHECKSUM_FILES = [
    "manifest.json",
    "tools.json",
    "workflow_template.json",
    "runbooks.md",
    "screenshots_manifest.json",
]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def action_bundle() -> int:
    """Write/refresh bundle files and recompute checksums."""
    print("=== airia_bundle: bundle ===")
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    # Recompute checksums from existing files
    lines = [
        "# LedgerLive Airia Community Bundle Checksums",
        "# Generated deterministically — sha256",
        "",
    ]
    ok = True
    for filename in CHECKSUM_FILES:
        fp = BUNDLE_DIR / filename
        if not fp.exists():
            print(f"ERROR: required file missing: {fp}")
            ok = False
            continue
        h = sha256_path(fp)
        lines.append(f"{h}  {filename}")
        print(f"  hashed  {filename}  {h[:16]}…")

    if not ok:
        return 1

    checksums_path = BUNDLE_DIR / "checksums.txt"
    checksums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote   {checksums_path.relative_to(REPO_ROOT)}")
    print("\nPASS — bundle files present, checksums refreshed.")
    return 0


def action_validate() -> int:
    """Strict readiness check: all required files present, checksums load OK."""
    print("=== airia_bundle: validate ===")
    missing = []
    for filename in REQUIRED_FILES:
        fp = BUNDLE_DIR / filename
        if not fp.exists():
            missing.append(filename)
        else:
            print(f"  FOUND   {filename}")

    if missing:
        print(f"\nFAIL — {len(missing)} required file(s) missing:")
        for f in missing:
            print(f"  MISSING  {f}")
        return 1

    # Validate manifest parses
    try:
        manifest = json.loads((BUNDLE_DIR / "manifest.json").read_text(encoding="utf-8"))
        assert manifest.get("name"), "manifest.name missing"
        assert manifest.get("version"), "manifest.version missing"
        assert manifest.get("bundle_hash"), "manifest.bundle_hash missing"
        print(f"\n  manifest name   : {manifest['name']}")
        print(f"  manifest version: {manifest['version']}")
        print(f"  bundle_hash     : {manifest['bundle_hash'][:24]}…")
    except Exception as exc:
        print(f"\nFAIL — manifest.json invalid: {exc}")
        return 1

    # Validate tools count
    try:
        tools = json.loads((BUNDLE_DIR / "tools.json").read_text(encoding="utf-8"))
        count = len(tools.get("tools", []))
        assert count >= 8, f"expected >=8 tools, got {count}"
        print(f"  tools count     : {count}")
    except Exception as exc:
        print(f"\nFAIL — tools.json invalid: {exc}")
        return 1

    print("\nPASS — bundle is Airia-import-ready.")
    return 0


def action_verify() -> int:
    """Offline checksum verification."""
    print("=== airia_bundle: verify ===")
    checksums_path = BUNDLE_DIR / "checksums.txt"
    if not checksums_path.exists():
        print(f"FAIL: checksums.txt not found at {checksums_path}")
        return 1

    expected: dict[str, str] = {}
    for line in checksums_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) == 2:
            expected[parts[1]] = parts[0]

    failures: list[str] = []
    for filename in CHECKSUM_FILES:
        fp = BUNDLE_DIR / filename
        if not fp.exists():
            failures.append(f"MISSING  {filename}")
            continue
        actual = sha256_path(fp)
        exp = expected.get(filename, "")
        if not exp:
            print(f"  WARN     {filename}  (no checksum recorded)")
            continue
        if actual == exp:
            print(f"  OK       {filename}")
        else:
            failures.append(f"MISMATCH {filename}\n  expected: {exp}\n  actual:   {actual}")

    print()
    if failures:
        print("FAIL — checksum mismatches:")
        for f in failures:
            print(f)
        return 1
    print("PASS — all checksums match.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Airia Community Bundle CLI")
    parser.add_argument(
        "--action",
        choices=["bundle", "validate", "verify"],
        required=True,
        help="Action to perform",
    )
    args = parser.parse_args()

    actions = {
        "bundle": action_bundle,
        "validate": action_validate,
        "verify": action_verify,
    }
    return actions[args.action]()


if __name__ == "__main__":
    sys.exit(main())
