#!/usr/bin/env python3
"""Generate a timestamped proof pack for LedgerLive waves.

Usage:
    python tools/proof/generate_proof_pack.py [--wave-range 1-30]
    python tools/proof/generate_proof_pack.py --milestone golden-e2e
"""
import shutil, subprocess, sys, os, json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts" / "proof"


def run(cmd: str, cwd: str | None = None) -> tuple[int, str]:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       cwd=cwd or str(ROOT), timeout=300)
    return r.returncode, r.stdout + r.stderr


def main():
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Accept --milestone or --wave-range
    milestone = "base"
    if "--milestone" in sys.argv:
        idx = sys.argv.index("--milestone")
        milestone = sys.argv[idx + 1]
    elif "--wave-range" in sys.argv:
        idx = sys.argv.index("--wave-range")
        milestone = f"wave{sys.argv[idx + 1]}"

    pack_dir = ARTIFACTS / f"{ts}-{milestone}"
    pack_dir.mkdir(parents=True, exist_ok=True)

    # 1. PROJECT_ID check
    pid_file = ROOT / "PROJECT_ID"
    pid = pid_file.read_text().strip() if pid_file.exists() else "MISSING"
    assert pid == "LEDGERLIVE", f"PROJECT_ID mismatch: {pid}"

    # 2. Run gates
    gate1_rc, gate1_out = run(f"{sys.executable} tools/gates/no_apex_references.py")
    gate2_rc, gate2_out = run(f"{sys.executable} tools/gates/no_network_in_tests.py")

    # 3. Run pytest
    pytest_rc, pytest_out = run(
        f"{sys.executable} -m pytest tests/ -v --tb=short",
        cwd=str(ROOT / "apps" / "api")
    )

    # 4. Git info
    _, git_log = run("git log --oneline -20")
    _, git_tags = run("git tag --sort=-v:refname | head -30")

    # 5. File tree
    _, tree = run("git ls-files")

    # 6. Collect Playwright artifacts (screenshots, traces, videos, report)
    pw_report_src = ROOT / "apps" / "web" / "playwright-report"
    pw_screenshots_src = ROOT / "apps" / "web" / "test-results" / "screenshots"
    pw_traces_src = ROOT / "apps" / "web" / "test-results"

    playwright_meta: dict = {"screenshots": [], "traces": [], "videos": []}

    if pw_screenshots_src.exists():
        screenshots_dst = pack_dir / "screenshots"
        screenshots_dst.mkdir(exist_ok=True)
        for f in sorted(pw_screenshots_src.glob("*.png")):
            shutil.copy2(f, screenshots_dst / f.name)
            playwright_meta["screenshots"].append(f.name)

    if pw_traces_src.exists():
        trace_files = list(pw_traces_src.rglob("trace.zip"))
        traces_dst = pack_dir / "traces"
        if trace_files:
            traces_dst.mkdir(exist_ok=True)
        for i, f in enumerate(trace_files[:10]):
            dest_name = f"{i:02d}-{f.parent.name}-trace.zip"
            shutil.copy2(f, traces_dst / dest_name)
            playwright_meta["traces"].append(dest_name)

        video_files = list(pw_traces_src.rglob("*.webm"))
        videos_dst = pack_dir / "videos"
        if video_files:
            videos_dst.mkdir(exist_ok=True)
        for i, f in enumerate(video_files[:5]):
            dest_name = f"{i:02d}-{f.parent.name}.webm"
            shutil.copy2(f, videos_dst / dest_name)
            playwright_meta["videos"].append(dest_name)

    if pw_report_src.exists() and (pw_report_src / "index.html").exists():
        pw_report_dst = pack_dir / "playwright-report"
        shutil.copytree(pw_report_src, pw_report_dst, dirs_exist_ok=True)
        playwright_meta["html_report"] = "playwright-report/index.html"

    # Write pack
    manifest = {
        "timestamp": ts,
        "milestone": milestone,
        "project_id": pid,
        "gates": {
            "no_apex_references": {"rc": gate1_rc, "pass": gate1_rc == 0},
            "no_network_in_tests": {"rc": gate2_rc, "pass": gate2_rc == 0},
        },
        "pytest": {"rc": pytest_rc, "pass": pytest_rc == 0},
        "playwright": playwright_meta,
    }

    (pack_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (pack_dir / "gate_no_apex.txt").write_text(gate1_out)
    (pack_dir / "gate_no_network.txt").write_text(gate2_out)
    (pack_dir / "pytest_output.txt").write_text(pytest_out)
    (pack_dir / "git_log.txt").write_text(git_log)
    (pack_dir / "git_tags.txt").write_text(git_tags)
    (pack_dir / "file_tree.txt").write_text(tree)

    all_pass = gate1_rc == 0 and gate2_rc == 0 and pytest_rc == 0
    status = "ALL PASS" if all_pass else "FAILURES DETECTED"
    ss_count = len(playwright_meta["screenshots"])
    print(f"\nProof pack: {pack_dir}")
    print(f"Status: {status}")
    print(f"Screenshots collected: {ss_count}")
    print(json.dumps(manifest, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
