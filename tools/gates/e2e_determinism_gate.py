#!/usr/bin/env python3
"""
tools/gates/e2e_determinism_gate.py

Determinism Hard Gate — two modes:

MODE 1: Compare two Playwright JSON result files
    python tools/gates/e2e_determinism_gate.py <run1.json> <run2.json>

MODE 2: API round-trip (requires running server)
    python tools/gates/e2e_determinism_gate.py --api http://127.0.0.1:8090

    Mode 2 performs two independent reset → seed → assert cycles and compares
    the assertion payloads.  No Playwright required.

Exits 0   if both runs are identical.
Exits 1   if any mismatch is found (prints diff to stderr).
Exits 2   on argument / parsing error.
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path


# ── Shared helpers ──────────────────────────────────────────────────────────

def _print_ok(msg: str) -> None:
    print(f"  OK  {msg}")


def _print_fail(msg: str) -> None:
    print(f"  FAIL  {msg}", file=sys.stderr)


# ── MODE 1: JSON file comparison ────────────────────────────────────────────

def load_results(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def summarise(data: dict) -> dict:
    """Extract determinism-relevant metrics from a Playwright JSON report."""
    stats = data.get("stats", {})
    suites = data.get("suites", [])

    titles_passed: list[str] = []
    titles_failed: list[str] = []
    titles_skipped: list[str] = []

    def walk(suite_list):
        for suite in suite_list:
            for spec in suite.get("specs", []):
                for test in spec.get("tests", []):
                    status = test.get("status", "")
                    title = f"{suite.get('title', '')} > {spec.get('title', '')}"
                    if status == "passed":
                        titles_passed.append(title)
                    elif status in ("failed", "timedOut", "interrupted"):
                        titles_failed.append(title)
                    elif status in ("skipped", "pending"):
                        titles_skipped.append(title)
            walk(suite.get("suites", []))

    walk(suites)

    return {
        "passed": stats.get("expected", len(titles_passed)),
        "failed": stats.get("unexpected", len(titles_failed)),
        "skipped": stats.get("skipped", len(titles_skipped)),
        "passed_titles": sorted(titles_passed),
        "failed_titles": sorted(titles_failed),
    }


def compare_summaries(s1: dict, s2: dict, label1: str, label2: str) -> bool:
    ok = True

    def check(key: str, label: str):
        nonlocal ok
        if s1[key] != s2[key]:
            _print_fail(
                f"[{label}] {label1}={s1[key]}  vs  {label2}={s2[key]}"
            )
            ok = False
        else:
            _print_ok(f"[{label}]: {s1[key]}")

    check("passed", "passed count")
    check("failed", "failed count")
    check("skipped", "skipped count")

    set1, set2 = set(s1["passed_titles"]), set(s2["passed_titles"])
    only_in_1 = sorted(set1 - set2)
    only_in_2 = sorted(set2 - set1)
    if only_in_1 or only_in_2:
        ok = False
        if only_in_1:
            _print_fail(f"[titles only in {label1}]: {only_in_1}")
        if only_in_2:
            _print_fail(f"[titles only in {label2}]: {only_in_2}")
    else:
        _print_ok(f"[test titles]: {len(set1)} unique titles match")

    if s1["failed_titles"] != s2["failed_titles"]:
        ok = False
        _print_fail(
            f"[failed titles] {label1}={s1['failed_titles']}  vs  {label2}={s2['failed_titles']}"
        )
    elif s1["failed_titles"]:
        print(f"  NOTE [same failures in both]: {s1['failed_titles']}")
    else:
        _print_ok("[failed titles]: none in either run")

    return ok


def run_json_mode(path1: str, path2: str) -> None:
    data1 = load_results(path1)
    data2 = load_results(path2)
    s1 = summarise(data1)
    s2 = summarise(data2)

    print(f"\n── Determinism Gate (JSON mode) ─────────────────────────────")
    print(f"  run1: {path1}")
    print(f"  run2: {path2}")
    print(f"─────────────────────────────────────────────────────────────")

    ok = compare_summaries(s1, s2, "run1", "run2")
    _finish(ok)


# ── MODE 2: API round-trip ───────────────────────────────────────────────────

def _api(base: str, method: str, path: str, data: bytes | None = None) -> dict:
    url = f"{base.rstrip('/')}{path}"
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        print(f"ERROR: {method} {url} → {exc.code}: {body}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"ERROR: {method} {url} → {exc}", file=sys.stderr)
        sys.exit(2)


def _seed_and_assert(base: str, label: str) -> dict:
    """Reset → seed → return assertions payload."""
    print(f"  [{label}] resetting…", end=" ", flush=True)
    _api(base, "POST", "/api/ops/golden-scenario-reset")
    print("seeding…", end=" ", flush=True)
    seed = _api(base, "POST", "/api/ops/golden-scenario-run")
    assert seed.get("status") == "seeded", f"Unexpected seed status: {seed}"
    print("asserting…", end=" ", flush=True)
    assertions = _api(base, "GET", "/api/ops/e2e-assertions")
    print("done")
    return assertions


def compare_assertions(a1: dict, a2: dict) -> bool:
    ok = True
    all_keys = sorted(set(a1.keys()) | set(a2.keys()))
    for key in all_keys:
        v1, v2 = a1.get(key, "MISSING"), a2.get(key, "MISSING")
        if v1 != v2:
            _print_fail(f"[{key}] run1={v1!r}  vs  run2={v2!r}")
            ok = False
        else:
            _print_ok(f"[{key}]: {v1!r}")
    return ok


def run_api_mode(base: str) -> None:
    print(f"\n── Determinism Gate (API mode) ──────────────────────────────")
    print(f"  api: {base}")
    print(f"─────────────────────────────────────────────────────────────")

    a1 = _seed_and_assert(base, "run1")
    a2 = _seed_and_assert(base, "run2")

    print()
    ok = compare_assertions(a1, a2)
    _finish(ok)


# ── Entry point ─────────────────────────────────────────────────────────────

def _finish(ok: bool) -> None:
    if ok:
        print("\n✓ DETERMINISM GATE PASSED\n")
        sys.exit(0)
    else:
        print("\n✗ DETERMINISM GATE FAILED (see above)\n", file=sys.stderr)
        sys.exit(1)


def main():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == "--api":
        run_api_mode(args[1])
    elif len(args) == 2 and not args[0].startswith("--"):
        run_json_mode(args[0], args[1])
    else:
        print(
            "Usage:\n"
            "  python tools/gates/e2e_determinism_gate.py <run1.json> <run2.json>\n"
            "  python tools/gates/e2e_determinism_gate.py --api http://127.0.0.1:8090",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
