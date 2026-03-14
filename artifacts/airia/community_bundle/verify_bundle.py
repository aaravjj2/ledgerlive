#!/usr/bin/env python3
"""
verify_bundle.py — Offline checksum verifier for the Airia community bundle.

Usage:
    python artifacts/airia/community_bundle/verify_bundle.py

Exit 0 = PASS (all checksums match)
Exit 1 = FAIL (one or more mismatches, diff printed to stdout)
"""

import hashlib
import json
import sys
from pathlib import Path

BUNDLE_DIR = Path(__file__).parent
CHECKSUMS_FILE = BUNDLE_DIR / "checksums.txt"

FILES_TO_VERIFY = [
    "manifest.json",
    "tools.json",
    "workflow_template.json",
    "runbooks.md",
    "screenshots_manifest.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_checksums(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) == 2:
            checksum, filename = parts
            result[filename] = checksum
    return result


def main() -> int:
    print("=== LedgerLive Airia Bundle Verifier ===")
    print(f"Bundle dir: {BUNDLE_DIR}\n")

    if not CHECKSUMS_FILE.exists():
        print(f"FAIL: checksums file not found: {CHECKSUMS_FILE}")
        return 1

    expected = load_checksums(CHECKSUMS_FILE)
    failures: list[str] = []

    for filename in FILES_TO_VERIFY:
        filepath = BUNDLE_DIR / filename
        if not filepath.exists():
            failures.append(f"MISSING  {filename}")
            continue

        actual = sha256_file(filepath)
        exp = expected.get(filename, "")

        if not exp:
            # File exists but no checksum recorded — treat as soft warning, not failure
            print(f"WARN     {filename}  (no checksum recorded)")
            continue

        if actual == exp:
            print(f"OK       {filename}")
        else:
            failures.append(f"MISMATCH {filename}\n  expected: {exp}\n  actual:   {actual}")

    print()
    if failures:
        print("=== FAIL ===")
        for f in failures:
            print(f)
        return 1

    print("=== PASS — all checksums match ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
