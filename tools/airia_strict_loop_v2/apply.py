"""apply.py — Deterministic fix planner for brutal_evaluation.json (v2).

Reads the structured judge output, maps failures to concrete repo actions,
and applies fixes. NEVER edits the judge score directly.

Usage:
    python tools/airia_strict_loop_v2/apply.py --from brutal_evaluation.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def load_evaluation(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fix_from_failed_checks(failed: list[str]) -> list[str]:
    """Map failed check names to actionable fixes."""
    actions: list[str] = []

    if "ingestion" in failed:
        actions.append("VERIFY: demo_seed must populate documents on startup")

    if "documents" in failed:
        actions.append("SEED: ensure at least 1 document in w03_document_store")

    if "ocr" in failed:
        actions.append("SEED: ensure OCR jobs with status=completed in w04_ocr_pipeline")

    if "exceptions_ai" in failed:
        actions.append("SEED: ensure exceptions have AI classification fields")

    if "reconciliation" in failed:
        actions.append("SEED: ensure reconciliation records exist in w06_reconciliation")

    if "reasoning" in failed:
        actions.append("SEED: workflow seed data must include reasoning traces")

    if "resolve" in failed:
        actions.append("FIX: exception resolve endpoint must accept POST and return 200")

    if "llm_called" in failed:
        actions.append("INFO: LLM signals detected via code scan — verify OLLAMA_MODEL is set")

    if "race_control" in failed:
        actions.append("FIX: /api/race-control router must be included in main.py")

    if "demo_script" in failed:
        demo_path = REPO / "DEMO.md"
        if not demo_path.exists():
            actions.append("CREATE: DEMO.md scripted walkthrough needed")

    if "video" in failed:
        actions.append("NOTE: No video demo found — record a 90s walkthrough (*.mp4)")

    if "webhooks" in failed:
        actions.append("FIX: webhook endpoints must appear in /openapi.json")

    if "mcp" in failed:
        actions.append("FIX: MCP endpoints must appear in /openapi.json")

    if "airia_called" in failed:
        actions.append("FIX: airia_webhook.py must have requests.post with airia pattern")

    if "cfo_cockpit" in failed:
        actions.append("FIX: /api/cfo/cockpit must be live and return cost_cap.runway_usd > 0")

    if "f1_scenario" in failed:
        actions.append("FIX: /api/cfo/scenario must return >= 5 invoices and >= 2 exceptions_before")

    if "ask_engineer" in failed:
        actions.append("FIX: POST /api/agent/ask must return answer + citations")

    if "story_mode" in failed:
        actions.append("FIX: /api/cfo/story-mode must return >= 5 steps")

    if "cfo_summary" in failed:
        actions.append("FIX: /api/race-control cfo_cockpit.cfo_summary must be truthy")

    return actions


def fix_from_criticisms(criticisms: list[dict]) -> list[str]:
    """Extract action items from LLM negative criticisms."""
    actions: list[str] = []
    for crit in criticisms:
        msg = crit.get("message", "")
        code = crit.get("code", "")
        if code == "cfo_not_memorable":
            actions.append("CRITICAL: CFO would not remember demo — ensure server running for judge")
        elif code == "not_submission_ready":
            actions.append("CRITICAL: Submission not ready — check all evidence checks pass")
        elif code == "llm_issue":
            actions.append(f"LLM ISSUE: {msg}")
    return actions


def apply_root_cleanup() -> list[str]:
    """Move test-*.png and rc-page-*.png from root to artifacts/debug/."""
    actions: list[str] = []
    debug_dir = REPO / "artifacts" / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)

    for pattern in ["test-*.png", "rc-page-*.png"]:
        for f in REPO.glob(pattern):
            dest = debug_dir / f.name
            shutil.move(str(f), str(dest))
            actions.append(f"MOVED: {f.name} -> artifacts/debug/")

    return actions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="eval_file", default="brutal_evaluation.json")
    args = parser.parse_args()

    eval_path = REPO / args.eval_file
    if not eval_path.exists():
        print(f"[apply-v2] {eval_path} not found — nothing to fix.")
        sys.exit(0)

    ev = load_evaluation(str(eval_path))
    all_actions: list[str] = []

    # 1. Map failed checks to actions
    failed = ev.get("failed_checks", [])
    all_actions.extend(fix_from_failed_checks(failed))

    # 2. Map LLM criticisms to actions
    criticisms = ev.get("negative_criticisms", [])
    all_actions.extend(fix_from_criticisms(criticisms))

    # 3. Root cleanup
    all_actions.extend(apply_root_cleanup())

    print(f"\n[apply-v2] {len(all_actions)} actions identified:")
    for i, action in enumerate(all_actions, 1):
        print(f"  {i}. {action}")

    # Write action log
    log_path = REPO / "artifacts" / "airia" / "fix_actions_v2.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "actions": all_actions,
            "source": args.eval_file,
            "failed_checks": failed,
            "score": ev.get("computed_score", 0),
            "cfo_remember": ev.get("cfo_remember", "NO"),
            "submission_ready": ev.get("submission_ready", "NO"),
        }, f, indent=2)

    print(f"\n[apply-v2] Action log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
