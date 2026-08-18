# SPDX-License-Identifier: MIT
"""Haelt die Lizenzentscheidung E08 dauerhaft fest.

anonymizer-modul ist MIT-lizenziert und PUBLIC (github.com/ellmos-ai/anonymizer).
PyMuPDF (`fitz`) steht unter AGPL-3.0 -- eine geerbte Copyleft-Bindung, die in
einem als MIT ausgewiesenen, gebuendelten Modul nicht implizit auftauchen darf.

Anders als bei anderen Modulen (siehe doc-services/tests/test_no_agpl.py) ist
PyMuPDF hier NICHT vollstaendig ersetzt: `_anonymize_pdf()` (die PDF-Schwaerzung)
braucht PyMuPDFs Content-Stream-Redaktion, um sensible Textstellen tatsaechlich
aus dem PDF zu entfernen (nicht nur visuell zu ueberdecken) -- eine gleichwertige
Neuimplementierung mit rein permissiven Bibliotheken war zum Zeitpunkt von
Entscheidung E08 (2026-08-18) nicht mit vertretbarer Sicherheitsgarantie machbar
(siehe README, Abschnitt "PDF-Schwaerzung").

Statt AGPL implizit zu erben, wird die Grenze hier EXPLIZIT gezogen:
  - PDF-Scan (Erkennung sensibler Daten): pypdf (BSD-3-Clause) -- kein PyMuPDF.
  - PDF-Verschluesselung: pikepdf (MPL-2.0) -- kein PyMuPDF.
  - PDF-Schwaerzung (_anonymize_pdf): PyMuPDF, eigenes Extra "pdf-redact",
    NICHT Teil von "pdf" oder "all" -- wer es installiert, bindet sich bewusst.

Dieser Test haelt zwei Dinge fest: (1) fitz/PyMuPDF taucht NIRGENDS ausserhalb
von core.py und dort NUR im deklarierten Import-Block und in _anonymize_pdf
auf -- die Grenze bleibt exakt so eng wie deklariert, auch nach kuenftigen
Aenderungen. (2) pyproject.toml haelt PyMuPDF aus "pdf" und "all" heraus.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE = REPO_ROOT / "anonymizer_modul"
CORE = PACKAGE / "core.py"

# Die einzige Methode, in der fitz/PyMuPDF-Namen ausserhalb des Import-Blocks
# vorkommen duerfen (Entscheidung E08).
ALLOWED_METHOD = "_anonymize_pdf"

VERBOTENE_WURZELN = {"fitz", "pymupdf", "PyMuPDF"}


def _parse(pfad: Path) -> ast.Module:
    return ast.parse(pfad.read_text(encoding="utf-8"), filename=str(pfad))


def test_paket_hat_dateien():
    assert list(PACKAGE.rglob("*.py")), "Kein Quelltext gefunden -- Testpfad pruefen"


@pytest.mark.parametrize(
    "datei",
    sorted(p for p in PACKAGE.rglob("*.py") if p != CORE),
    ids=lambda p: p.name,
)
def test_kein_copyleft_import_ausserhalb_core(datei: Path):
    """Kein Modul ausser core.py importiert PyMuPDF."""
    baum = _parse(datei)
    getroffen: list[str] = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            for alias in knoten.names:
                wurzel = alias.name.split(".")[0]
                if wurzel in VERBOTENE_WURZELN:
                    getroffen.append(wurzel)
        elif isinstance(knoten, ast.ImportFrom) and knoten.module:
            wurzel = knoten.module.split(".")[0]
            if wurzel in VERBOTENE_WURZELN:
                getroffen.append(wurzel)
    assert not getroffen, (
        f"{datei.relative_to(REPO_ROOT)} importiert PyMuPDF: {getroffen}. "
        "Die AGPL-Grenze ist auf core.py::_anonymize_pdf beschraenkt (E08)."
    )


def test_fitz_in_core_bleibt_auf_anonymize_pdf_beschraenkt():
    """Innerhalb core.py darf 'fitz' NUR im Top-Level-Import-Try/Except und
    innerhalb von _anonymize_pdf vorkommen -- keine dritte Fundstelle."""
    baum = _parse(CORE)

    erlaubte_bereiche: list[tuple[int, int]] = []

    gefunden_methode = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == ALLOWED_METHOD:
            gefunden_methode = True
            erlaubte_bereiche.append((knoten.lineno, knoten.end_lineno))
    assert gefunden_methode, f"{ALLOWED_METHOD} nicht gefunden -- Testpfad pruefen"

    # Der deklarierte Top-Level-Import-Block: ein `try:` dessen Rumpf `import fitz` enthaelt.
    gefunden_import_block = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Try):
            if any(
                isinstance(stmt, ast.Import) and any(a.name == "fitz" for a in stmt.names)
                for stmt in knoten.body
            ):
                gefunden_import_block = True
                erlaubte_bereiche.append((knoten.lineno, knoten.end_lineno))
    assert gefunden_import_block, "Kein try/except-Block mit 'import fitz' gefunden"

    def erlaubt(lineno: int) -> bool:
        return any(start <= lineno <= end for start, end in erlaubte_bereiche)

    abweichler = [
        knoten.lineno
        for knoten in ast.walk(baum)
        if isinstance(knoten, ast.Name) and knoten.id == "fitz" and not erlaubt(knoten.lineno)
    ]
    assert not abweichler, (
        f"'fitz' ausserhalb des Import-Blocks und von {ALLOWED_METHOD} verwendet, "
        f"Zeilen: {abweichler}. Die AGPL-Grenze (E08) waere damit ueberschritten."
    )


def test_pdf_scan_nutzt_pypdf():
    """Positivprobe: extract_text_from_file() nutzt pypdf, nicht fitz."""
    quelle = CORE.read_text(encoding="utf-8")
    match = re.search(r"def extract_text_from_file.*?(?=\n    def )", quelle, re.DOTALL)
    assert match, "extract_text_from_file() nicht gefunden"
    body = match.group(0)
    assert "PdfReader" in body, "extract_text_from_file() soll pypdf.PdfReader nutzen"
    assert "fitz" not in body, "extract_text_from_file() darf kein fitz mehr verwenden"


def test_pyproject_pdf_und_all_extras_ohne_pymupdf():
    """'pdf' und 'all' duerfen PyMuPDF nicht (mehr) ziehen; nur 'pdf-redact' darf."""
    quelle = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    try:
        import tomllib
    except ModuleNotFoundError:  # Python < 3.11
        import tomli as tomllib  # type: ignore[no-redef]
    daten = tomllib.loads(quelle)
    extras = daten["project"]["optional-dependencies"]

    for name in ("pdf", "all"):
        deps = " ".join(extras.get(name, [])).lower()
        assert "pymupdf" not in deps, f"Extra '{name}' zieht PyMuPDF: {extras.get(name)}"

    redact_deps = " ".join(extras.get("pdf-redact", [])).lower()
    assert "pymupdf" in redact_deps, "Extra 'pdf-redact' soll PyMuPDF fuehren"
