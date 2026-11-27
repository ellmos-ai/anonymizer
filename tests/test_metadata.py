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
    assert re.search(r"2026-\d{2}-\d{2}", content), "llms.txt must contain a valid check date"


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


def test_badges_and_ci_workflow_links():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    ci_badge = "https://github.com/ellmos-ai/anonymizer/actions/workflows/ci.yml/badge.svg"
    ci_workflow_url = "https://github.com/ellmos-ai/anonymizer/actions/workflows/ci.yml"

    assert ci_badge in readme_en, "CI badge missing in README.md"
    assert ci_badge in readme_de, "CI badge missing in README_de.md"
    assert ci_workflow_url in readme_en, "CI workflow link missing in README.md"
    assert ci_workflow_url in readme_de, "CI workflow link missing in README_de.md"
    assert "code style-ruff" in readme_en or "code%20style-ruff" in readme_en
    assert "code style-ruff" in readme_de or "Code--Stil-ruff" in readme_de

def test_pep561_typing_marker_and_package_data():
    typed_marker = REPO_ROOT / "anonymizer_modul" / "py.typed"
    assert typed_marker.is_file(), "PEP 561 marker anonymizer_modul/py.typed must exist"

    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'anonymizer_modul = ["py.typed"]' in pyproject, "pyproject.toml must declare package-data for py.typed"
    assert '"Typing :: Typed"' in pyproject, "pyproject.toml classifiers must declare Typing :: Typed"


def test_manifest_in_completeness():
    manifest_file = REPO_ROOT / "MANIFEST.in"
    assert manifest_file.is_file(), "MANIFEST.in must exist"
    content = manifest_file.read_text(encoding="utf-8")

    assert "include README.md" in content
    assert "include README_de.md" in content
    assert "include llms.txt" in content
    assert "include THIRD_PARTY_LICENSES.md" in content
    assert "include anonymizer_modul/py.typed" in content
    assert "recursive-include assets *.png *.svg" in content
    assert "exclude LOCK*.txt" in content


def test_ci_matrix_minimum_python_coverage():
    ci_file = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    content = ci_file.read_text(encoding="utf-8")
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert 'requires-python = ">=3.10"' in pyproject
    assert 'python-version: ["3.10", "3.11", "3.12"]' in content or "3.10" in content
    assert "pip check" in content, "ci.yml must verify dependency integrity"
    assert "build:" in content, "ci.yml must include distribution build job"


def test_pyproject_pep639_and_agpl_isolation():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    # PEP 639 license compliance: license is string, no conflicting OSI classifier
    assert 'license = "MIT"' in pyproject
    assert "License :: OSI Approved" not in pyproject

    # E08 invariant: "all" extra must remain AGPL-free
    assert '"pdf-redact" = ["PyMuPDF' in pyproject
    all_block = re.search(r'all\s*=\s*\[(.*?)\]', pyproject, re.DOTALL).group(1)
    assert "PyMuPDF" not in all_block, "'all' extra must never contain PyMuPDF (AGPL isolation)"


def test_security_policy_sla_and_private_reporting():
    security_file = REPO_ROOT / "SECURITY.md"
    assert security_file.is_file(), "SECURITY.md must exist at repo root"
    content = security_file.read_text(encoding="utf-8")

    assert "0.3.1" in content
    assert "https://github.com/ellmos-ai/anonymizer/security/advisories/new" in content
    assert "INV-SLA-09" in content
    assert "INV-SLA-10" in content
    assert "48 hours" in content and "48 Stunden" in content
    assert "5 business days" in content and "5 Werktagen" in content
    assert "30 calendar days" in content and "30 Kalendertagen" in content
    assert "kein eigenes Git-Repository" not in content
    assert "Version 0.3.0 ist der einzige" not in content


def test_dependabot_supply_chain_config():
    dependabot = REPO_ROOT / ".github" / "dependabot.yml"
    assert dependabot.is_file(), ".github/dependabot.yml must exist"
    content = dependabot.read_text(encoding="utf-8")

    assert 'package-ecosystem: "pip"' in content
    assert 'package-ecosystem: "github-actions"' in content
    assert 'interval: "weekly"' in content
    assert "open-pull-requests-limit:" in content


def test_gitignore_security_and_gate_entries():
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    lines = {ln.strip() for ln in gitignore.splitlines() if ln.strip() and not ln.startswith("#")}

    for required in (
        "__pycache__/",
        "*.pyc",
        ".env",
        "*.db",
        ".venv/",
        ".idea/",
        ".vscode/",
        "data/",
        "keys/",
        "*.schluessel.enc",
        "*.pem",
        "*.p12",
        "*.pfx",
        "*.secret",
        "*.token",
        "id_rsa*",
        "id_ed25519*",
        "*-IDEAPAD-GEI*",
        "CONFLICT_REVIEW_LOG*",
    ):
        assert required in lines, f"Missing security/gate entry in .gitignore: {required}"

    assert "TODO.md" not in lines, "Public 10-gate TODO.md must not be excluded by .gitignore"


def test_todo_status_table_and_zero_secrets_or_personal_paths():
    todo_file = REPO_ROOT / "TODO.md"
    assert todo_file.is_file(), "TODO.md must exist at repo root"
    todo_text = todo_file.read_text(encoding="utf-8")
    assert "## STATUS" in todo_text
    assert "| Category | Status | Notes |" in todo_text
    assert "10/10" in todo_text

    secret_assign = re.compile(
        r"(?:API_KEY|TOKEN|PASSWORD|SECRET|PRIVATE_KEY)\s*=\s*"
        r'(?P<q>["\'])(?P<val>[^"\']{8,})(?P=q)',
        re.IGNORECASE,
    )
    token_patterns = [
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),
        re.compile(r"ghp_[a-zA-Z0-9]{36,}"),
        re.compile(r"gho_[a-zA-Z0-9]{36,}"),
        re.compile(r"-----BEGIN " + r"[A-Z0-9_\s-]*PRIVATE KEY-----"),
    ]
    personal_paths = [
        re.compile(r"C:[\\/]+Users[\\/]+(?!Public\b|Default\b)[A-Za-z0-9._-]+", re.IGNORECASE),
        re.compile(r"/c/Users/(?!Public\b|Default\b)[A-Za-z0-9._-]+", re.IGNORECASE),
        re.compile(r"/home/(?!runner\b)[A-Za-z0-9._-]+", re.IGNORECASE),
    ]
    skip_dirs = {
        ".git",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        "anonymizer_modul.egg-info",
        "_after-care",
        "_intern",
        "keys",
        "klienten",
        "_ausgabe",
        "data",
        ".anonymizer",
        ".gemini",
        ".antigravity",
        ".claude",
        ".cursor",
        ".copilot",
    }
    binary_exts = {
        ".png",
        ".svg",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".pdf",
        ".whl",
        ".gz",
        ".zip",
        ".pyc",
        ".pyo",
        ".pyd",
        ".db",
        ".sqlite",
        ".sqlite3",
        ".enc",
        ".bak",
        ".tmp",
    }
    sentinels = {"CHANGE-ME-IN-PRODUCTION"}

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(REPO_ROOT).parts
        if any(part in skip_dirs or part.endswith(".egg-info") for part in rel_parts):
            continue
        if path.name in {
            "MARKETING-LOG.txt",
            "REPO.pointer.json",
            "anonymizer.repo.md",
            "pytest_result.txt",
        }:
            continue
        if path.name.startswith(("LOCK", "CONFLICT_REVIEW_LOG")):
            continue
        if path.suffix.lower() in binary_exts:
            continue

        rel_str = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in secret_assign.finditer(line):
                assert match.group("val") in sentinels, (
                    f"Non-sentinel secret assignment in {rel_str}:{lineno}"
                )
            for tok_re in token_patterns:
                assert not tok_re.search(line), f"Secret token pattern in {rel_str}:{lineno}"
            for path_re in personal_paths:
                assert not path_re.search(line), f"Hardcoded personal path in {rel_str}:{lineno}"


def test_cli_help_and_version_parity(capsys):
    import pytest
    from anonymizer_modul import __version__
    from anonymizer_modul.core import main

    with pytest.raises(SystemExit) as help_exit:
        main(["--help"])
    assert help_exit.value.code == 0
    help_out = capsys.readouterr().out
    assert f"v{__version__}" in help_out
    assert "v0.2.5" not in help_out

    with pytest.raises(SystemExit) as ver_exit:
        main(["--version"])
    assert ver_exit.value.code == 0
    ver_out = capsys.readouterr().out
    assert __version__ in ver_out

    core_text = (REPO_ROOT / "anonymizer_modul" / "core.py").read_text(encoding="utf-8")
    assert "nicht verfuegbar" not in core_text


def test_pyproject_build_requires_pep639_and_pytest_strictness():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires = ["setuptools>=77.0.3", "wheel"]' in pyproject
    assert "--strict-markers" in pyproject
    assert "--strict-config" in pyproject
    assert "--basetemp" not in pyproject
    assert '".pytest_temp"' in pyproject
    assert '".pytest_tmp"' in pyproject


def test_ci_python_313_and_wheel_verification():
    ci_text = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert '"3.13"' in ci_text
    assert "anonymizer_modul/py.typed" in ci_text
    assert "Verify wheel packaging integrity" in ci_text


def test_generate_fake_date_never_zero_offset():
    from anonymizer_modul.core import _generate_fake_date_same_age

    for _ in range(500):
        fake, offset = _generate_fake_date_same_age("15.03.2016")
        assert offset != 0
        assert fake != "15.03.2016"
