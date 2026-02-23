#!/usr/bin/env python3
"""Generate a timestamped proof pack for LedgerLive waves.

Usage: python tools/proof/generate_proof_pack.py [--wave-range 1-30]
"""
import subprocess, sys, os, json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts" / "proof"


def run(cmd: str, cwd: str | None = None) -> tuple[int, str]:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       cwd=cwd or str(ROOT), timeout=300)
    return r.returncode, r.stdout + r.stderr


def main():
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    wave_range = "base"
    if "--wave-range" in sys.argv:
        idx = sys.argv.index("--wave-range")
        wave_range = sys.argv[idx + 1]

    pack_dir = ARTIFACTS / f"{ts}-wave{wave_range}"
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

    # Write pack
    manifest = {
        "timestamp": ts,
        "wave_range": wave_range,
        "project_id": pid,
        "gates": {
            "no_apex_references": {"rc": gate1_rc, "pass": gate1_rc == 0},
            "no_network_in_tests": {"rc": gate2_rc, "pass": gate2_rc == 0},
        },
        "pytest": {"rc": pytest_rc, "pass": pytest_rc == 0},
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
    print(f"\nProof pack: {pack_dir}")
    print(f"Status: {status}")
    print(json.dumps(manifest, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())

