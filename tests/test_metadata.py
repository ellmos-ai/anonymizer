"""Contract tests for repository metadata, bilingual documentation, and governance invariants.

Enforces Policy P-006 (bilingual README architecture), HOOK-BANNER-ASSET-01
(Mermaid linting & asset guardrails), CI matrix and least-privilege permissions,
lock-system protection, and core architectural invariants.
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
    assert re.search(r"2026-09-\d{2}", content), "llms.txt must contain a valid 2026-09 check date"


def test_pyproject_metadata_urls():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file()
    content = pyproject_path.read_text(encoding="utf-8")

    assert 'Homepage = "https://github.com/ellmos-ai/anonymizer"' in content
    assert 'Changelog = "https://github.com/ellmos-ai/anonymizer/blob/main/CHANGELOG.md"' in content
    assert 'Security = "https://github.com/ellmos-ai/anonymizer/blob/main/SECURITY.md"' in content
    assert '"Parent Organization" = "https://github.com/ellmos-ai"' in content
    assert '"Umbrella Ecosystem" = "https://github.com/open-bricks"' in content
    assert '"Third-Party Licenses" = "https://github.com/ellmos-ai/anonymizer/blob/main/THIRD_PARTY_LICENSES.md"' in content
    assert '"LLM Ready" = "https://raw.githubusercontent.com/ellmos-ai/anonymizer/main/llms.txt"' in content
    assert '"German Documentation" = "https://github.com/ellmos-ai/anonymizer/blob/main/README_de.md"' in content


def test_ci_workflows_hardening():
    ci_file = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_file.is_file(), "CI workflow .github/workflows/ci.yml must exist"
    content = ci_file.read_text(encoding="utf-8")

    # Top-level least-privilege permissions
    assert "permissions:\n  contents: read" in content or "permissions:\n  contents: read" in content.replace("\r\n", "\n")

    # Top-level concurrency
    assert "concurrency:" in content
    assert "cancel-in-progress: true" in content

    # Job timeouts
    for job_name in ("test:", "test-pdf-redact:", "lint:", "bandit:"):
        assert job_name in content, f"Job {job_name} missing from ci.yml"

    timeout_matches = re.findall(r"timeout-minutes:\s*15", content)
    assert len(timeout_matches) >= 4, f"Expected at least 4 jobs with timeout-minutes: 15, found {len(timeout_matches)}"


def test_community_workflows_exist():
    workflows_dir = REPO_ROOT / ".github" / "workflows"
    stale = workflows_dir / "stale.yml"
    welcome = workflows_dir / "welcome.yml"

    assert stale.is_file(), "stale.yml must exist in .github/workflows/"
    assert welcome.is_file(), "welcome.yml must exist in .github/workflows/"

    stale_content = stale.read_text(encoding="utf-8")
    welcome_content = welcome.read_text(encoding="utf-8")

    assert "issues: write" in stale_content and "pull-requests: write" in stale_content
    assert "issues: write" in welcome_content and "pull-requests: write" in welcome_content
    assert "timeout-minutes:" in stale_content
    assert "timeout-minutes:" in welcome_content


def test_gitignore_lock_and_multihost_patterns():
    gitignore_file = REPO_ROOT / ".gitignore"
    assert gitignore_file.is_file()
    content = gitignore_file.read_text(encoding="utf-8")

    # Lock patterns
    assert "LOCK" in content
    assert "LOCK.user.*" in content
    assert "LOCK.until.*" in content
    assert "LOCK-CACHE.md" in content

    # Multi-host conflict patterns
    assert "*conflicted copy*" in content
    assert "*-ASUS*" in content
    assert "*-WORKSTATION*" in content
    assert "*-Mac Studio*" in content

    # Dependency lock exclusions
    assert "uv.lock" in content
    assert "!package-lock.json" in content


def test_license_and_third_party_sbom():
    license_file = REPO_ROOT / "LICENSE"
    third_party_file = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    pyproject_file = REPO_ROOT / "pyproject.toml"

    assert license_file.is_file(), "LICENSE file must exist"
    assert third_party_file.is_file(), "THIRD_PARTY_LICENSES.md must exist"

    pyproject_content = pyproject_file.read_text(encoding="utf-8")
    assert 'license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]' in pyproject_content

    sbom_content = third_party_file.read_text(encoding="utf-8")
    assert "cryptography" in sbom_content
    assert "defusedxml" in sbom_content
    assert "pypdf" in sbom_content
    assert "pikepdf" in sbom_content
    assert "openpyxl" in sbom_content
    assert "spacy" in sbom_content
    assert "PyMuPDF" in sbom_content


def test_manifest_version_parity():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    mod_v1 = (REPO_ROOT / "ellmos-module.json").read_text(encoding="utf-8")
    mod_v2 = (REPO_ROOT / "ellmos-module.v2.json").read_text(encoding="utf-8")
    init_file = (REPO_ROOT / "anonymizer_modul" / "__init__.py").read_text(encoding="utf-8")

    v_pyproject = re.search(r'version\s*=\s*"([^"]+)"', pyproject).group(1)
    v_mod_v1 = re.search(r'"version":\s*"([^"]+)"', mod_v1).group(1)
    v_mod_v2 = re.search(r'"version":\s*"([^"]+)"', mod_v2).group(1)
    v_init = re.search(r'__version__\s*=\s*"([^"]+)"', init_file).group(1)

    assert v_pyproject == "0.3.1", f"pyproject.toml version is {v_pyproject}, expected 0.3.1"
    assert v_mod_v1 == "0.3.1", f"ellmos-module.json version is {v_mod_v1}, expected 0.3.1"
    assert v_mod_v2 == "0.3.1", f"ellmos-module.v2.json version is {v_mod_v2}, expected 0.3.1"
    assert v_init == "0.3.1", f"__init__.py version is {v_init}, expected 0.3.1"


def test_statutory_bgb_notice_in_readmes():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "§ 521 BGB" in readme_en, "English README.md must contain § 521 BGB liability notice"
    assert "§ 521 BGB" in readme_de, "German README_de.md must contain § 521 BGB liability notice"
