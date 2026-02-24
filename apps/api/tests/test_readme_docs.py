"""test_readme_docs.py — README + docs F1 theme + Airia content assertions.

Validates that README.md has:
- F1 glossary table with required terms
- Airia section
- 3-step quickstart

Validates that docs/airia/ has required files.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
README = REPO_ROOT / "README.md"
DOCS_AIRIA = REPO_ROOT / "docs" / "airia"


# ── F1 Glossary ──────────────────────────────────────────────────────────────

F1_TERMS = [
    "Race Control",
    "Pit Stop",
    "Telemetry",
    "Safety Car",
    "Court Pack",
    "DRS Zone",
    "Incident",
    "Pit Wall",
]


def test_readme_exists():
    assert README.exists(), "README.md must exist"


def test_readme_has_f1_glossary():
    text = README.read_text(encoding="utf-8")
    assert "F1 Glossary" in text, "README must contain 'F1 Glossary' heading"


@pytest.mark.parametrize("term", F1_TERMS)
def test_readme_f1_term(term: str):
    text = README.read_text(encoding="utf-8")
    assert term in text, f"README F1 Glossary must include term: {term!r}"


def test_readme_has_airia_section():
    text = README.read_text(encoding="utf-8")
    assert "Why Airia" in text or "Airia" in text, "README must reference Airia"


def test_readme_has_quickstart():
    text = README.read_text(encoding="utf-8")
    assert "make demo" in text or "Quickstart" in text, "README must have quickstart"


def test_readme_has_williams_f1():
    text = README.read_text(encoding="utf-8")
    assert "Williams" in text or "F1" in text, "README must reference Williams F1"


# ── docs/airia/ ──────────────────────────────────────────────────────────────

REQUIRED_DOCS = [
    "AIRIA_OVERVIEW.md",
    "AIRIA_IMPORT.md",
    "F1_THEME.md",
]


@pytest.mark.parametrize("filename", REQUIRED_DOCS)
def test_docs_airia_file_exists(filename: str):
    path = DOCS_AIRIA / filename
    assert path.exists(), f"docs/airia/{filename} must exist"


def test_airia_overview_has_table():
    text = (DOCS_AIRIA / "AIRIA_OVERVIEW.md").read_text(encoding="utf-8")
    assert "Airia Platform Fit" in text or "Tool Registry" in text


def test_airia_import_has_bundle_structure():
    text = (DOCS_AIRIA / "AIRIA_IMPORT.md").read_text(encoding="utf-8")
    assert "manifest.json" in text
    assert "tools.json" in text
    assert "workflow_template.json" in text


def test_f1_theme_has_full_mapping():
    text = (DOCS_AIRIA / "F1_THEME.md").read_text(encoding="utf-8")
    for term in ["Race Control", "Pit Stop", "Court Pack", "Safety Car"]:
        assert term in text, f"F1_THEME.md must document term: {term!r}"
