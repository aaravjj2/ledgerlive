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


# ── v2 loop infrastructure ──────────────────────────────────────

def test_v2_loop_runner_exists():
    assert (REPO / "tools" / "airia_strict_loop_v2" / "run.ps1").exists()


def test_v2_apply_exists():
    assert (REPO / "tools" / "airia_strict_loop_v2" / "apply.py").exists()


def test_v2_apply_importable():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "apply_v2",
        str(REPO / "tools" / "airia_strict_loop_v2" / "apply.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "fix_from_failed_checks")
    assert hasattr(mod, "fix_from_criticisms")
    assert hasattr(mod, "main")


def test_v2_apply_maps_failed_checks():
    """fix_from_failed_checks generates actions for known check names."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "apply_v2_test",
        str(REPO / "tools" / "airia_strict_loop_v2" / "apply.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    actions = mod.fix_from_failed_checks(["cfo_cockpit", "ask_engineer", "story_mode"])
    assert len(actions) == 3
    assert any("cfo/cockpit" in a.lower() for a in actions)
    assert any("agent/ask" in a.lower() for a in actions)
    assert any("story-mode" in a.lower() for a in actions)


def test_makefile_has_strict_loop_v2():
    content = (REPO / "Makefile").read_text(encoding="utf-8")
    assert "airia\\:strict-loop-v2" in content or "airia:strict-loop-v2" in content


def test_docs_demo_cfo_exists():
    assert (REPO / "docs" / "DEMO_CFO.md").exists()
