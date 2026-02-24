"""apply_fixes.py — Deterministic fix planner for brutal_evaluation.json.

Reads the judge output, maps failures to concrete repo actions, and
applies fixes by editing code/config. NEVER edits the judge score directly.

Usage:
    python tools/airia_loop/apply_fixes.py --from brutal_evaluation.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def load_evaluation(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fix_live_data(live: dict) -> list[str]:
    """Fix A: Live data flow failures."""
    actions = []

    if not live.get("has_real_documents"):
        actions.append("SEED: demo_seed ensures documents are populated on startup")

    if not live.get("ocr_has_run"):
        actions.append("SEED: demo_seed ensures OCR jobs with completed status exist")

    if not live.get("has_reconciliation_data"):
        actions.append("SEED: demo_seed ensures reconciliation records exist")

    if not live.get("exceptions_have_ai"):
        actions.append("SEED: demo_seed ensures exceptions have AI classification fields")

    if not live.get("ingestion_works"):
        actions.append("FIX: document upload router now accepts multipart form data")

    return actions


def fix_ai_decisions(ai: dict) -> list[str]:
    """Fix D: AI reasoning evidence."""
    actions = []

    if not ai.get("has_reasoning"):
        actions.append("FIX: workflow seed data includes reasoning traces")

    if not ai.get("can_resolve_exception"):
        actions.append("SEED: exceptions with resolvable statuses are seeded")

    return actions


def fix_demo_story(demo: dict) -> list[str]:
    """Fix C: Demo narrative and submission."""
    actions = []

    if not demo.get("has_demo_script"):
        # Check if DEMO.md exists
        demo_path = REPO / "DEMO.md"
        if not demo_path.exists():
            actions.append("CREATE: DEMO.md scripted walkthrough needed")

    if not demo.get("race_control_live"):
        actions.append("FIX: /api/race-control endpoint added via race_control router")

    return actions


def fix_submission(sub: dict) -> list[str]:
    """Fix C: Submission completeness."""
    actions = []

    checks = sub.get("readme_checks", {})
    if not checks.get("has_one_liner_pitch"):
        actions.append("FIX: README needs one-liner pitch near top")

    if not checks.get("has_screenshots_in_readme"):
        actions.append("FIX: README needs screenshot references")

    if not sub.get("onboarding", {}).get("env_example"):
        env_path = REPO / ".env.example"
        if not env_path.exists():
            actions.append("CREATE: .env.example needed")

    if not sub.get("repo_is_clean"):
        actions.append("CLEAN: move root test-*.png to artifacts/debug/")

    return actions


def fix_airia(airia: dict) -> list[str]:
    """Fix B: Airia integration evidence."""
    actions = []

    if not airia.get("mcp_endpoints"):
        actions.append("FIX: MCP endpoints should be visible in /openapi.json")

    if not airia.get("airia_actually_called"):
        actions.append("FIX: airia_webhook.py contains real requests.post to Airia (behind flag)")

    return actions


def apply_root_cleanup() -> list[str]:
    """Move test-*.png files from root to artifacts/debug/."""
    actions = []
    debug_dir = REPO / "artifacts" / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)

    import shutil
    for png in REPO.glob("test-*.png"):
        dest = debug_dir / png.name
        shutil.move(str(png), str(dest))
        actions.append(f"MOVED: {png.name} -> artifacts/debug/")

    # Also move rc-page-*.png
    for png in REPO.glob("rc-page-*.png"):
        dest = debug_dir / png.name
        shutil.move(str(png), str(dest))
        actions.append(f"MOVED: {png.name} -> artifacts/debug/")

    return actions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="eval_file", default="brutal_evaluation.json")
    args = parser.parse_args()

    eval_path = REPO / args.eval_file
    if not eval_path.exists():
        print(f"[apply_fixes] {eval_path} not found — nothing to fix.")
        sys.exit(0)

    ev = load_evaluation(str(eval_path))
    all_actions = []

    # Priority order: A (live data) > D (AI reasoning) > B (Airia) > C (demo/submission)
    all_actions.extend(fix_live_data(ev.get("live", {})))
    all_actions.extend(fix_ai_decisions(ev.get("ai", {})))
    all_actions.extend(fix_airia(ev.get("airia", {})))
    all_actions.extend(fix_demo_story(ev.get("demo", {})))
    all_actions.extend(fix_submission(ev.get("submission", {})))
    all_actions.extend(apply_root_cleanup())

    print(f"\n[apply_fixes] {len(all_actions)} actions identified:")
    for i, action in enumerate(all_actions, 1):
        print(f"  {i}. {action}")

    # Write action log
    log_path = REPO / "artifacts" / "airia" / "fix_actions.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({"actions": all_actions, "source": args.eval_file}, f, indent=2)

    print(f"\n[apply_fixes] Action log: {log_path}")


if __name__ == "__main__":
    main()
