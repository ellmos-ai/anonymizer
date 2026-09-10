"""Contract tests for repository metadata, bilingual documentation, and governance invariants.

Enforces Policy P-006 (bilingual README architecture), HOOK-BANNER-ASSET-01
(Mermaid linting & asset guardrails), and core architectural invariants.
"""

from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_readme_files_exist():
    readme_en = REPO_ROOT / "README.md"
    readme_de = REPO_ROOT / "README_de.md"
    assert readme_en.is_file(), "English README.md must exist at repo root"
    assert readme_de.is_file(), "German README_de.md must exist at repo root"


def test_banner_preserved():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")
    banner_file = REPO_ROOT / "assets" / "banner.png"

    assert banner_file.is_file(), "Header banner file assets/banner.png must exist"
    assert 'src="assets/banner.png"' in readme_en
    assert 'src="assets/banner.png"' in readme_de


def test_language_switchers():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "**English** | [Deutsch](README_de.md)" in readme_en
    assert "[English](README.md) | **Deutsch**" in readme_de


def test_navigation_sections_count():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    # Both documents must have 12 section links under Quick Navigation / Schnellnavigation
    en_links = re.findall(r"- \[([^\]]+)\]\(#([^\)]+)\)", readme_en)
    de_links = re.findall(r"- \[([^\]]+)\]\(#([^\)]+)\)", readme_de)

    assert len(en_links) == 12, f"Expected 12 English navigation links, found {len(en_links)}"
    assert len(de_links) == 12, f"Expected 12 German navigation links, found {len(de_links)}"


def test_invariants_coverage():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    for i in range(1, 11):
        inv_key = f"INV-LOCAL-{i:02d}"
        assert inv_key in readme_en, f"Missing {inv_key} in English README.md"
        assert inv_key in readme_de, f"Missing {inv_key} in German README_de.md"


def test_mermaid_diagrams_present():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    for text, name in [(readme_en, "README.md"), (readme_de, "README_de.md")]:
        assert "flowchart TD" in text, f"Flowchart missing in {name}"
        assert "sequenceDiagram" in text, f"Sequence diagram missing in {name}"
        assert "autonumber" in text, f"Sequence diagram autonumber missing in {name}"


def test_llms_txt_integrity():
    llms_path = REPO_ROOT / "llms.txt"
    assert llms_path.is_file(), "llms.txt must exist at repo root"
    content = llms_path.read_text(encoding="utf-8")

    assert "README.md" in content
    assert "README_de.md" in content
    assert "2026-09-10" in content


def test_pyproject_metadata_urls():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file()
    content = pyproject_path.read_text(encoding="utf-8")

    assert 'Homepage = "https://github.com/ellmos-ai/anonymizer"' in content
    assert 'Changelog = "https://github.com/ellmos-ai/anonymizer/blob/main/CHANGELOG.md"' in content
    assert 'Security = "https://github.com/ellmos-ai/anonymizer/blob/main/SECURITY.md"' in content
    assert '"Parent Organization" = "https://github.com/ellmos-ai"' in content
    assert '"Umbrella Ecosystem" = "https://github.com/open-bricks"' in content
