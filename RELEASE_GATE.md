# Release Gate — anonymizer 0.2.4

Stand: 2026-07-23 (vorherige Fassungen: 0.2.3, 0.2.2, 0.2.1 und 0.2.0/2026-07-16)

## Entscheidung

**Tech-Gates erfüllt. Public-Umschaltung: Operator-Entscheidung ausstehend.**

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
Mehrwort-/Anker-Logik greift. Gegen die echte RUN2-Referenzakte end-to-end
verifiziert (siehe Prüfgates unten).

Der fehlende OCR-Workflow für bildhaltige Inhalte bleibt ein bewusster,
dokumentierter Funktionsausschluss (fail-closed), kein offenes Gate. Die
tatsächliche Öffentlichstellung des Repositories (Push, Sichtbarkeit,
Ankündigung) ist ein separater, vom Operator zu treffender Schritt
(`/repo-publish-check` + Freigabe) und nicht Teil dieses technischen Gates.

## Prüfgates

| Gate | Ergebnis |
|---|---|
| Syntax/Import | grün — `py_compile` für Core und Schutztests |
| Vollständige Testsuite | grün — 65 bestanden, 2 OS-Skips (Windows-Symlinks, KEIN Modell-Test übersprungen), 14 Subtests (Stand 0.2.4, mit geladenem `de_core_news_lg` verifiziert) |
| Schutz-PoCs / alternative Eingaben | grün — Schutztests: OOXML-Attribute/Charts, NER (Lemma-Denyliste + POS-Struktur + Anker-Prinzip + Mehrwort-Lemma-Trim), Casing, PDF-TOC, Reparse, Template-Medien-Allowlist und atomare Veröffentlichung |
| CLI | grün — UTF-8-Selbsttest und installierte Wheel-Hilfe mit echten Unterbefehlen |
| Build und Archivinhalt | grün — isolierter sdist-/Wheel-Bau; keine Locks, Backups, Caches oder Bytecode im Wheel |
| Paketprüfung | grün (Stand 0.2.0; für 0.2.1–0.2.4 nicht erneut gebaut) — `pip check`; Twine auf diesem Host nicht installiert |
| Modulmanifeste | grün — gültiges JSON (`ellmos-module.json`/`.v2.json` auf 0.2.4 aktualisiert) |
| Unabhängiger Schlussreview | grün — 0×P0/P1/release-relevante P2 (0.1.0→0.2.0) |
| Git-Repository + CI | grün seit 2026-07-23 — Branch `main`, `.github/workflows/ci.yml` (Python 3.11/3.12 auf ubuntu-latest: Tests, Lint, Bandit) |
| Bandit (`bandit -r anonymizer_modul -ll`) | grün — 0 Medium/High nach defusedxml-Härtung (zuvor 3× Medium/B314) |
| Realer NER-Modelltest | grün — `de_core_news_lg`, 7/10 synthetische Namen erkannt (dokumentiert in `TODO.md`) |
| Template-Medien-Allowlist | grün seit 2026-07-23 — `trusted_template_path` (API/CLI/ENV), SHA-256-Hash-Verifikation gegen Referenz-Template |
| NER-Anker-Prinzip + Mehrwort-Härtung (0.2.3/0.2.4) | grün — End-to-End-Realcheck gegen die echte RUN2-Akte: kein Fehlklassen-Token ("Grob", "Umgang", "Klettverschlüsse", "Landkreises", "Einrichtungsangaben", "Begleitung", "Handlauf", "Zähneputzen", "Anziehen", "Essen") in Scan, Profil-Mapping oder anonymisierter Ausgabe; Profil-Mapping exakt {Kim, Beispiel, Kim Beispiel, Test-Fiktiv, Test-Mustermann, Sachbearbeiter-Fiktiv} |
| README Legal-/DSGVO-Abschnitt | grün seit 2026-07-23 — „Rechtlicher Rahmen und Verantwortung" (DSGVO, § 203 StGB, englische Kurzfassung) |
| Öffentliche Sichtbarkeit (Push/Release) | ausstehend — Operator-Entscheidung, kein Tech-Gate |

## Bekannte Restpunkte

- Zwei Symlink-Laufzeittests benötigen Windows-Entwicklermodus/Adminrechte;
  auf der neuen ubuntu-latest-CI sollten sie regulär laufen. Reparse-/
  Junction-Erkennung ist zusätzlich deterministisch getestet.
- OCR fehlt weiterhin bewusst; bildhaltige DOCX/XLSX/PDF-Inhalte werden
  fail-closed abgelehnt statt unvollständig anonymisiert.
- `en_core_web_lg` wurde beim NER-Realtest nicht installiert (nur
  `de_core_news_lg`, wie beauftragt); optional nachholbar. Die neuen
  POS-/Anker-basierten Regressionstests sind entsprechend nur gegen
  `de_core_news_lg` skip-guarded verifiziert; CI installiert das Modell
  nicht, diese Tests laufen daher nur lokal/mit installiertem Modell.
- Twine, Signierung und ein erneuter Wheel-Bau für 0.2.4 stehen lokal noch
  aus und sind kein Blocker für dieses Tech-Gate.
- Der NER-Filter bleibt eine Heuristik (POS-Tagging + Anker + Denyliste),
  kein 100%-Garant. Unentdeckte Drittpersonen-Einzelworte ohne Anker landen
  sichtbar in `ner_review_only` statt automatisch ersetzt zu werden —
  bewusster Kompromiss zugunsten von Textintegrität statt blinder
  Vollständigkeit; Betreiber sollten `ner_review_only` vor Weitergabe
  manuell prüfen.
