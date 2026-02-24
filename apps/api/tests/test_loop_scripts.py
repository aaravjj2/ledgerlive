"""Tests that loop scripts exist and are valid."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_loop_runner_exists():
    assert (REPO / "tools" / "airia_loop" / "run_strict_loop.ps1").exists()


def test_apply_fixes_exists():
    assert (REPO / "tools" / "airia_loop" / "apply_fixes.py").exists()


def test_mock_receiver_exists():
    assert (REPO / "tools" / "airia_loop" / "mock_airia_receiver.py").exists()


def test_demo_md_exists():
    assert (REPO / "DEMO.md").exists()


def test_env_example_exists():
    assert (REPO / ".env.example").exists()


def test_demo_seed_exists():
    from app.services.demo_seed import seed_all
    assert callable(seed_all)


def test_race_control_router_exists():
    from app.routers.race_control import router
    assert router is not None


def test_airia_webhook_module_exists():
    from app.services.airia_webhook import post_to_airia, get_webhook_log
    assert callable(post_to_airia)
    assert callable(get_webhook_log)
