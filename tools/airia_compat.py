#!/usr/bin/env python3
"""Airia Compatibility Report CLI — deterministic offline compat check.

Writes artifacts/airia/community_bundle/compat_report.json and prints summary.

Usage:
    python tools/airia_compat.py
    python tools/airia_compat.py --output path/to/compat_report.json

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Resolve repo root and add apps/api to path
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "apps" / "api"))

from app.services.airia_compat import run_compat_report, BUNDLE_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description="Airia Compatibility Report generator")
    parser.add_argument(
        "--output",
        default=str(BUNDLE_DIR / "compat_report.json"),
        help="Output path for the generated report JSON",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Airia Compatibility Report — LedgerLive")
    print("=" * 60)

    report = run_compat_report()

    # Write to output
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    # Print results
    print(f"\n  Overall: {report['overall']}")
    print(f"  Pass: {report['pass_count']}  Fail: {report['fail_count']}\n")
    for check in report["checks"]:
        icon = "✓" if check["passed"] else "✗"
        print(f"  [{icon}] {check['name']}")
        if not check["passed"]:
            print(f"       Reason: {check['reason']}")

    print(f"\n  bundle_sha256:           {report['bundle_sha256'][:32]}...")
    print(f"  blueprint_sha256:        {report['blueprint_sha256'][:32]}...")
    print(f"  tools_sha256:            {report['tools_sha256'][:32]}...")
    print(f"  report_signature_sha256: {report['report_signature_sha256'][:32]}...")
    print(f"\n  Output: {out_path}")
    print("=" * 60)

    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
