# Release Gate — anonymizer 0.3.0

Stand: 2026-08-18 (Inhalt der Prüfgates: 0.3.0/2026-08-18; vorherige Fassungen:
0.2.5/2026-07-23, 0.2.4, 0.2.3, 0.2.2, 0.2.1 und 0.2.0/2026-07-16)

## Entscheidung

**Tech-Gates erfüllt. Repository seit 2026-07-24 öffentlich.**

**0.3.0 — Lizenzgrenze PyMuPDF (Entscheidung E08, 2026-08-18, Ticket
T-20260818-775009068):** Das `pdf`-Extra führte bisher PyMuPDF (AGPL-3.0) als
Abhängigkeit eines MIT-lizenzierten, öffentlich gebündelten Moduls — geerbte
Copyleft, die genau bei Weiterverbreitung real bindet. `extract_text_from_file()`
(PDF-Scan) läuft jetzt über `pypdf` (BSD-3-Clause); PyMuPDF bleibt NUR für die
Content-Stream-Redaktion in `_anonymize_pdf()` und liegt dafür in einem
eigenen, ausdrücklich zu wählenden Extra `pdf-redact` — nicht mehr in `pdf`
oder `all`. Begründung, warum diese eine Funktion nicht mit rein permissiven
Bibliotheken ersetzt wurde: README, Abschnitt „PDF-Schwärzung: Lizenzgrenze".
Neuer Wächter-Test `tests/test_no_agpl.py` hält die Grenze fest (PyMuPDF nur
im Import-Block und in `_anonymize_pdf`; `pdf`/`all` ohne PyMuPDF). CI läuft
jetzt in zwei Jobs: Standard (`[all,dev]`, AGPL-frei) und `test-pdf-redact`
(`[pdf-redact,dev]`, deckt `TestPdfBoundary` weiterhin ab).

**Lokale Verifikation der 0.3.0-Änderung** (separate, frische venv, keine
spaCy-Sprachmodelle installiert — Modelle sind von dieser Änderung nicht
betroffen, siehe bestehende Skip-Guards):
- Ohne PyMuPDF (`pip install -e ".[all,dev]"`): **66 bestanden, 12 Skips**
  (3× PyMuPDF fehlt wie erwartet, 7× fehlendes Sprachmodell, 2× fehlende
  Windows-Symlink-Rechte — alle 12 bereits vor 0.3.0 vorhanden).
  `test_no_agpl.py` (5 Tests) grün.
- Mit PyMuPDF zusätzlich installiert (`[pdf-redact]`): **69 bestanden, 9
  Skips** — `TestPdfBoundary` (3 Tests, echte Content-Stream-Redaktion,
  Metadaten-/Annotation-/Attachment-Entfernung, Bild-Fail-Closed,
  Verschlüsselungs-Fallback-Schutz) läuft grün, funktional unverändert
  gegenüber 0.2.5.
- Negativprobe: `fitz` testweise außerhalb von `_anonymize_pdf` referenziert
  → `test_no_agpl.py` schlägt reproduzierbar an; Testcode danach entfernt.
- `ruff check .`: grün. `bandit -r anonymizer_modul -ll`: 0 Medium/High
  (11 Low, wie zuvor). `py_compile`: grün.

Die Datenschutzgrenzen sind lokal verifiziert. Der unabhängige Ausgangsreview
(0.1.0→0.2.0) fand 3×P1 und 3×release-relevante P2; die gezielten Nachchecks
endeten mit **0×P0/P1/release-relevante P2**. Seit 2026-07-23 sind zusätzlich
Git-Repository, CI (Test-Matrix/Lint/Bandit), realer NER-Modelltest und die
Legal-/DSGVO-Ergänzung im README vorhanden; ein zuvor gefundener
Bandit-Medium-Befund (XML-Parsing ohne defusedxml, 3× B314) wurde durch
Umstellung auf `defusedxml.ElementTree` behoben.

Ein foerderplaner-Referenzlauf (RUN1/RUN2/RUN3) deckte drei reale Defekte
auf: (1) Template-Bilder blockierten die Ver-/De-Anonymisierung
unconditional — behoben durch `trusted_template_path`-Hash-Allowlist. (2)
Der NER-Plausibilitätsfilter war zunächst nur eine Wortlisten-Allowlist
(0.2.2-Symptom-Fix). (3) **0.2.2 selbst erwies sich in RUN3 als real
SCHLECHTER als 0.2.1** — reines POS==PROPN als Akzeptanzkriterium kippt in
der Praxis zu durchlässig, spaCy misstaggt Substantive in Aufzählungs-/
Fachtext-Kontexten häufig als PROPN. 0.2.3 ersetzt das durch das
Anker-Prinzip (Operator-Design): Mehrwort-NER-Spans gelten als verifiziert,
Einzelwort-Spans brauchen einen Anker (Lexikon-Vorname oder vorangehendes
Titel-/Anrede-Token) — ohne Anker keine destruktive Ersetzung, stattdessen
sichtbarer, nicht-destruktiver Review-Kandidat. RUN4 zeigte einen
verbleibenden Feinschliff: Mehrwort-Spans umgingen das Anker-Prinzip noch
("Beim Anziehen", "Landkreises Lörrach"). 0.2.4 kürzt Gattungsbegriff-/
Verb-Lemma-Tokens (per Lemma-Gegenprobe) aus jedem Span, BEVOR die
Mehrwort-/Anker-Logik greift.

**RUN5 widerlegte 0.2.4 reproduzierbar in einer anderen Umgebung**
(System-Python statt eigener venv) — Root-Cause-Diagnose ergab KEINE
spaCy-/Modellversions-Drift (identisch: spacy 3.8.14, de_core_news_lg
3.8.0), sondern ob zusätzlich `en_core_web_lg` installiert ist: dieses
Modell taggt deutschen Fließtext eigenständig fehlerhaft als PERSON/PROPN
mit unzuverlässigem Lemma, wogegen die POS-/Lemma-Verteidigung (0.2.2-0.2.4)
nicht greift, weil sie auf deutsche Regeln zugeschnitten ist. 0.2.5 ergänzt
eine modellversions-robuste Oberflächen-Härtung (Kontraktionswörter,
Gattungsbegriff-Präfixmatch, deutsches Vokabular-Check), die unabhängig von
POS/Lemma und damit unabhängig vom installierten Modell greift. Gegen die
synthetische RUN2-Referenzakte end-to-end in BEIDEN Umgebungen (mit und ohne
`en_core_web_lg`) verifiziert (siehe Prüfgates unten).

Der fehlende OCR-Workflow für bildhaltige Inhalte bleibt ein bewusster,
dokumentierter Funktionsausschluss (fail-closed), kein offenes Gate. Die
Öffentlichstellung des Repositories ist seit 2026-07-24 vollzogen. Für 0.3.0
wird ein Versions-Tag gesetzt (siehe Prüfgates); eine etwaige
Paketveröffentlichung (Wheel/Twine) bleibt davon getrennt offen.

## Prüfgates

| Gate | Ergebnis |
|---|---|
| Syntax/Import | grün — `py_compile` für Core und Schutztests |
| Vollständige Testsuite | grün in BEIDEN Umgebungen — eigene venv (nur `de_core_news_lg`): 70 bestanden/3 Skips; System-Python (zusätzlich `en_core_web_lg`): 71 bestanden/2 Skips. Beide Male nur die 2 Windows-Symlink-OS-Limitationen, KEIN Modell-Test übersprungen |
| Schutz-PoCs / alternative Eingaben | grün — Schutztests: OOXML-Attribute/Charts, NER (Lemma-Denyliste + POS-Struktur + Anker-Prinzip + Mehrwort-Lemma-Trim + modellversions-robuste Oberflächen-Härtung), Casing, PDF-TOC, Reparse, Template-Medien-Allowlist und atomare Veröffentlichung |
| CLI | grün — UTF-8-Selbsttest und installierte Wheel-Hilfe mit echten Unterbefehlen |
| Build und Archivinhalt | grün — isolierter sdist-/Wheel-Bau; keine Locks, Backups, Caches oder Bytecode im Wheel |
| Paketprüfung | grün (Stand 0.2.0; für 0.2.1–0.3.0 nicht erneut gebaut) — `pip check`; Twine auf diesem Host nicht installiert |
| Modulmanifeste | grün — gültiges JSON (`ellmos-module.json`/`.v2.json` auf 0.3.0 aktualisiert, PyMuPDF-Extra-Zuordnung ergänzt) |
| AGPL-Lizenzgrenze (E08) | grün — `tests/test_no_agpl.py`; siehe Testlauf-Nachweis unten |
| Unabhängiger Schlussreview | grün — 0×P0/P1/release-relevante P2 (0.1.0→0.2.0) |
| Git-Repository + CI | grün seit 2026-07-23 — Branch `main`, `.github/workflows/ci.yml` (Python 3.11/3.12 auf ubuntu-latest: Tests, Lint, Bandit) |
| Bandit (`bandit -r anonymizer_modul -ll`) | grün — 0 Medium/High nach defusedxml-Härtung (zuvor 3× Medium/B314) |
| Realer NER-Modelltest | grün — `de_core_news_lg`, 7/10 synthetische Namen erkannt (dokumentiert in `CHANGELOG.md` 0.2.1) |
| Template-Medien-Allowlist | grün seit 2026-07-23 — `trusted_template_path` (API/CLI/ENV), SHA-256-Hash-Verifikation gegen Referenz-Template |
| NER-Anker-Prinzip + Mehrwort-/Oberflächen-Härtung (0.2.3–0.2.5) | grün in BEIDEN Umgebungen — End-to-End-Realcheck gegen die vollständige synthetische Referenzakte (RUN2): kein Fehlklassen-Token ("Grob", "Umgang", "Klettverschlüsse", "Landkreises", "Einrichtungsangaben", "Begleitung", "Handlauf", "Zähneputzen", "Anziehen", "Essen", "Kurze Notiz") BESTAETIGT (destruktiv ersetzt); Profil-Mapping korrekt (Kim, Beispiel, Kim Beispiel + fiktive Drittpersonen); alle Fehlklassen-Phrasen wörtlich unverändert im anonymisierten Output |
| README Legal-/DSGVO-Abschnitt | grün seit 2026-07-23 — „Rechtlicher Rahmen und Verantwortung" (DSGVO, § 203 StGB, englische Kurzfassung) |
| README Modellversions-Sensitivität | grün seit 2026-07-23 — empfohlene/getestete Version, `en_core_web_lg`-Risikohinweis, Versions-Pin-Kommentar in `pyproject.toml` |
| Öffentliche Sichtbarkeit | erledigt — Repository seit 2026-07-24 öffentlich unter `ellmos-ai/anonymizer` |
| Versions-Tag / GitHub-Release | grün — `v0.3.0` gesetzt und gepusht (0.2.5 blieb ungetaggt, siehe Historie oben) |

## Bekannte Restpunkte

- Zwei Symlink-Laufzeittests benötigen Windows-Entwicklermodus/Adminrechte;
  auf der neuen ubuntu-latest-CI sollten sie regulär laufen. Reparse-/
  Junction-Erkennung ist zusätzlich deterministisch getestet.
- OCR fehlt weiterhin bewusst; bildhaltige DOCX/XLSX/PDF-Inhalte werden
  fail-closed abgelehnt statt unvollständig anonymisiert.
- CI installiert kein spaCy-Modell; die POS-/Anker-/Oberflächen-basierten
  Regressionstests sind entsprechend skip-guarded und laufen nur lokal/mit
  installiertem Modell. Der `en_core_web_lg`-spezifische Test läuft nur,
  wenn dieses Modell zusätzlich installiert ist (empirisch auf diesem Host
  in System-Python der Fall, in der projekteigenen venv bewusst nicht).
- Twine, Signierung und ein erneuter Wheel-Bau für 0.3.0 stehen lokal noch
  aus und sind kein Blocker für dieses Tech-Gate.
- Der NER-Filter bleibt eine Heuristik (POS-Tagging + Anker + Oberflächen-
  Härtung + Denyliste), kein 100%-Garant. Unentdeckte Drittpersonen-
  Einzelworte ohne Anker landen sichtbar in `ner_review_only` statt
  automatisch ersetzt zu werden — bewusster Kompromiss zugunsten von
  Textintegrität statt blinder Vollständigkeit; Betreiber sollten
  `ner_review_only` vor Weitergabe manuell prüfen. Empfehlung:
  `en_core_web_lg` nur installieren, wenn tatsächlich Englisch anonymisiert
  wird (siehe README „Modellversions-Sensitivität").
