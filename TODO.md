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
| Public Release | gesperrt | privates Modul; kein eigenes Git-Repository und kein Legal/Privacy-Release |

## Public-Fahrplan (User-Entscheidung 2026-07-23: veröffentlichen nach
worksheet-generator + Berichts-Kern)

- [ ] Git-Repo initialisieren (Review-/Signaturprozess), CI (Lint+Tests,
  Unix-Runner für Symlink-Tests), Bandit/Twine.
- [ ] Realer NER-Modelltest (de_core_news_lg/en_core_web_lg, synthetisch).
- [ ] README-Ergänzungen für Public: § 203 StGB-Verantwortungshinweis für
  Berufsgeheimnisträger, DSGVO-Einordnung (Pseudonymisierung ≠ Anonymisierung).
- [ ] Release-Gates via /repo-publish-check → User-Freigabe → Public (MIT).

## Offen

- [ ] Den realen foerderplaner-Konsumenten in einem separaten, gelockten Lauf
  gegen den strikten NER-/Medienvertrag integrieren und dessen eigene veraltete
  Dokumentation bereinigen.
- [ ] Einen kontrollierten OCR-Workflow definieren, bevor bildhaltige
  DOCX/XLSX/PDF-Dateien als anonymisierbar gelten dürfen.
- [ ] Mit installierten `de_core_news_lg`- und `en_core_web_lg`-Modellen einen
  realistischen, ausschließlich synthetischen NER-Qualitätstest ausführen.
- [ ] Entscheiden, ob der Privatbereich bewusst ohne Git bleibt oder ein
  separates privates Repository mit Review-/Signaturprozess erhält.

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
