# Release Gate — anonymizer 0.2.1

Stand: 2026-07-23 (vorherige Fassung: 0.2.0, 2026-07-16)

## Entscheidung

**Tech-Gates erfüllt. Public-Umschaltung: Operator-Entscheidung ausstehend.**

Die Datenschutzgrenzen sind lokal verifiziert. Der unabhängige Ausgangsreview
(0.1.0→0.2.0) fand 3×P1 und 3×release-relevante P2; die gezielten Nachchecks
endeten mit **0×P0/P1/release-relevante P2**. Seit 2026-07-23 sind zusätzlich
Git-Repository, CI (Test-Matrix/Lint/Bandit), realer NER-Modelltest und die
Legal-/DSGVO-Ergänzung im README vorhanden; ein zuvor gefundener
Bandit-Medium-Befund (XML-Parsing ohne defusedxml, 3× B314) wurde durch
Umstellung auf `defusedxml.ElementTree` behoben. Der fehlende OCR-Workflow für
bildhaltige Inhalte bleibt ein bewusster, dokumentierter Funktionsausschluss
(fail-closed), kein offenes Gate. Die tatsächliche Öffentlichstellung des
Repositories (Push, Sichtbarkeit, Ankündigung) ist ein separater, vom Operator
zu treffender Schritt (`/repo-publish-check` + Freigabe) und nicht Teil dieses
technischen Gates.

## Prüfgates

| Gate | Ergebnis |
|---|---|
| Syntax/Import | grün — `py_compile` für Core und Schutztests |
| Vollständige Testsuite | grün — 58 bestanden, 2 OS-Skips, 3 Subtests bestanden (Stand 0.2.1, nach defusedxml-Umstellung + Template-Medien-/NER-Plausibilitätsfix erneut verifiziert) |
| Schutz-PoCs / alternative Eingaben | grün — 31 Schutztests: OOXML-Attribute/Charts, NER, Casing, PDF-TOC, Reparse und atomare Veröffentlichung |
| CLI | grün — UTF-8-Selbsttest und installierte Wheel-Hilfe mit echten Unterbefehlen |
| Build und Archivinhalt | grün — isolierter sdist-/Wheel-Bau; keine Locks, Backups, Caches oder Bytecode im Wheel |
| Paketprüfung | grün (Stand 0.2.0; für 0.2.1 nicht erneut gebaut) — `pip check`; Twine auf diesem Host nicht installiert |
| Modulmanifeste | grün — gültiges JSON (`ellmos-module.json`/`.v2.json` auf 0.2.1 aktualisiert) |
| Unabhängiger Schlussreview | grün — 0×P0/P1/release-relevante P2 (0.1.0→0.2.0) |
| Git-Repository + CI | grün seit 2026-07-23 — Branch `main`, `.github/workflows/ci.yml` (Python 3.11/3.12 auf ubuntu-latest: Tests, Lint, Bandit) |
| Bandit (`bandit -r anonymizer_modul -ll`) | grün seit 2026-07-23 — 0 Medium/High nach defusedxml-Härtung (zuvor 3× Medium/B314) |
| Realer NER-Modelltest | grün seit 2026-07-23 — `de_core_news_lg`, 7/10 synthetische Namen erkannt, dokumentiert in `TODO.md` |
| README Legal-/DSGVO-Abschnitt | grün seit 2026-07-23 — „Rechtlicher Rahmen und Verantwortung" (DSGVO, § 203 StGB, englische Kurzfassung) |
| Öffentliche Sichtbarkeit (Push/Release) | ausstehend — Operator-Entscheidung, kein Tech-Gate |

## Bekannte Restpunkte

- Zwei Symlink-Laufzeittests benötigen Windows-Entwicklermodus/Adminrechte;
  auf der neuen ubuntu-latest-CI sollten sie regulär laufen. Reparse-/
  Junction-Erkennung ist zusätzlich deterministisch getestet.
- OCR fehlt weiterhin bewusst; bildhaltige DOCX/XLSX/PDF-Inhalte werden
  fail-closed abgelehnt statt unvollständig anonymisiert.
- `en_core_web_lg` wurde beim NER-Realtest nicht installiert (nur
  `de_core_news_lg`, wie beauftragt); optional nachholbar.
- Twine, Signierung und ein erneuter Wheel-Bau für 0.2.1 stehen lokal noch
  aus und sind kein Blocker für dieses Tech-Gate.
