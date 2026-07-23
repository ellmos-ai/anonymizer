# TODO — anonymizer

Stand: 2026-07-16, Version 0.2.0

## Status

| Bereich | Status | Beleg |
|---|---|---|
| Standalone-Import | grün | Keine BACH-Laufzeitimports; Smoke-Test vorhanden |
| Datenschutzgrenze | grün mit dokumentierten Limits | `tests/test_security_boundaries.py`, `SECURITY_REVIEW_2026-07-16.md` |
| Schlüsselablage | grün | Cloud-/Traversal-/Symlink-Grenzen und atomare verschlüsselte Ablage |
| Formate | grün, fail-closed | DOCX/XLSX/PDF-Restdaten- und Medienkontrollen |
| CLI | grün | echte Unterbefehle, verdeckte Geheimnisse, belastbare Exitcodes |
| Public Release | Tech-Gates erfüllt, Freigabe ausstehend | Git+CI+Legal-Text+NER-Realtest seit 2026-07-23 grün; offen: /repo-publish-check, User-Freigabe, Umschalten `visibility`/Beschreibung von "privat" |

## Public-Fahrplan (User-Entscheidung 2026-07-23: veröffentlichen nach
worksheet-generator + Berichts-Kern)

- [x] 2026-07-23: Git-Repo initialisiert (Branch `main`, Initial-Commit
  `2ef2e11`), `.github/workflows/ci.yml` angelegt (Python 3.11/3.12-Matrix
  auf `ubuntu-latest` löst die 2 Windows-Symlink-Skips; Lint-Job mit
  ruff + py_compile-Fallback; Bandit-Job `bandit -r anonymizer_modul -ll`).
  Twine bleibt manueller Schritt vor dem eigentlichen PyPI-Release, kein
  CI-Job. Kein Remote/Push — macht der Operator.
- [x] 2026-07-23: Realer NER-Modelltest mit `de_core_news_lg` (spaCy 3.8.14)
  gegen 10 ausschließlich synthetische Namen (Testperson Beispielmann u. a.)
  in einem sozialpädagogischen Beispieltext: **7/10 Nachnamen erkannt**
  (`Anke Testlehrer`, `Beispielmann`, `Erika Musterfrau`, `Finn
  Beispielkind`, `Johann Mustermann`, `Klaus Erfundenmann`, `Thomas
  Musterleiter`). Nicht erkannt: `Fallbeispiel` (nur Vorname „Petra"
  erfasst), `Testfall` (Titel „Dr." vor dem Namen störte offenbar die
  Erkennung), `Testkind`. Modell lädt und arbeitet korrekt; Erkennungsrate
  ist modelltypisch nicht vollständig — bestätigt die bestehende
  „keine Garantie vollständiger Erkennung"-Formulierung in README/SECURITY.
  `en_core_web_lg` wurde in diesem Lauf nicht installiert (nicht angefordert,
  ~500 MB zusätzlich); NER_MODELS bleibt für beide Sprachen konfiguriert.
- [x] 2026-07-23: README-Ergänzung „Rechtlicher Rahmen und Verantwortung":
  Pseudonymisierung ≠ Anonymisierung (Art. 4 Nr. 5, 5, 6, 24, 32 DSGVO),
  § 203 StGB-Hinweis für Berufsgeheimnisträger, englische Kurzfassung
  („Legal note (English summary)") am Abschnittsende.
- [ ] Release-Gates via /repo-publish-check → User-Freigabe → Public (MIT).
  Weiterhin offen: `ellmos-module.json`/`pyproject.toml` tragen noch
  `visibility: "private"` bzw. eine `PRIVAT:`-Beschreibung — bewusst nicht
  automatisch umgeschaltet, das ist der eigentliche Public-Freigabeschritt.

## Offen

- [ ] Den realen foerderplaner-Konsumenten in einem separaten, gelockten Lauf
  gegen den strikten NER-/Medienvertrag integrieren und dessen eigene veraltete
  Dokumentation bereinigen.
- [ ] Einen kontrollierten OCR-Workflow definieren, bevor bildhaltige
  DOCX/XLSX/PDF-Dateien als anonymisierbar gelten dürfen.
- [ ] Optional: NER-Test zusätzlich mit `en_core_web_lg` wiederholen (in
  diesem Lauf nicht installiert, siehe Public-Fahrplan).
- [ ] **CI-Blocker:** `bandit -r anonymizer_modul -ll` (neuer CI-Job) schlägt
  lokal mit 3× Medium/B314 fehl: `xml.etree.ElementTree.fromstring` in
  `core.py:592/631/668` parst OOXML-Daten (DOCX/XLSX = ZIP+XML) ohne
  `defusedxml` — bei böswillig präparierten Eingabedateien potenziell
  XML-Entity-/Billion-Laughs-anfällig. Nicht selbständig gepatcht (sicherheits-
  kritischer Kernpfad, gehört in den etablierten Review-Prozess wie
  `SECURITY_REVIEW_2026-07-16.md`). Fix-Optionen: `defusedxml.ElementTree`
  statt `xml.etree.ElementTree` an den 3 Stellen, oder begründetes `# nosec
  B314` falls die Zip-/Größenlimits vorgelagert bereits ausreichend schützen
  — muss geprüft werden. Bis dahin bleibt der Bandit-Job im CI rot.
- [x] 2026-07-23: Git-Entscheidung getroffen — eigenes Repo (Branch `main`)
  im Modulordner selbst initialisiert statt separatem Privatbereich.

## Erledigt

- [x] 2026-07-16: Vollständiger Privacy-/Security-Review des 0.1.0-Snapshots;
  fail-closed Ordnerveröffentlichung, Pfad-/Symlink-/Cloud-Grenzen,
  transaktionale Einzeldatei-Verarbeitung, sichere Schlüsseldateien,
  vollständige Übernahme erkannter Namen/Institutionen und Domain-unabhängige
  E-Mail-Erkennung umgesetzt.
- [x] 2026-07-16: DOCX-/XLSX-OOXML-Flächen, PDF-Metadaten/Annotationen/Anhänge,
  Medienstopps, Ressourcenlimits, Restdatenprüfung und CLI-Vertrag mit
  Regressionstests abgesichert.
- [x] 2026-07-16: Unabhängigen Abschlussreview nachgearbeitet: NER-Modell- und
  Treffergrenzen, paketweite OOXML-Discovery inklusive Attribute/Charts,
  E-Mail-Casing, PDF-Bookmarks/Page-Labels, Windows-Reparse-Points und atomare
  Zielbaum-Veröffentlichung geschlossen; final 0×P0/P1/release-relevante P2.
- [x] 2026-07-16: README, WIRING, Manifest, Lizenz, Changelog, Security- und
  Release-Gate-Dokumentation auf den tatsächlichen Stand synchronisiert.
- [x] 2026-07-12: Wortgrenzen, Tabellenzeilen-Erkennung, Legacy-DOC,
  Absatz-Ersetzung und native Excel-Datumszellen aus dem BACH-Vorfall
  übernommen.
- [x] 2026-07-05: Build-Backend und Root-Übersicht gepflegt.
