#!/usr/bin/env python3
"""Generate golden binder baseline hash.

Run from apps/api/:
    python tools/generate_baseline.py

Requires app to be importable (run with pytest context or after pip install -e .)
"""
import sys
import pathlib

# Add apps/api to sys.path
HERE = pathlib.Path(__file__).resolve()
API_ROOT = HERE.parents[2] / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

# Trigger app initialization via test infrastructure
import pytest

# Use pytest to call the generation function
code = """
import pytest
@pytest.fixture(autouse=True)
def _init(tmp_path):
    pass

def test_generate_baseline():
    from app.services.golden_scenario import service, BASELINE_PATH
    service.reset()
    service.seed()
    h = service.write_baseline_binder_hash()
    print(f"\\nBaseline hash written: {h}")
    print(f"Path: {BASELINE_PATH}")
    assert h.startswith("sha256:")
"""

if __name__ == "__main__":
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-s", "-x", "--tb=short",
         "--override-ini=python_files=generate_baseline.py",
         __file__],
        cwd=str(API_ROOT),
    )
    sys.exit(result.returncode)
