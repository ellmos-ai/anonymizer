# Changelog

## 0.2.1 — 2026-07-23

- Git-Repository initialisiert (Branch `main`), GitHub-Actions-CI angelegt
  (Python 3.11/3.12-Matrix auf ubuntu-latest, Lint-Job, Bandit-Job).
- OOXML-Parsing gehärtet: `xml.etree.ElementTree` durch `defusedxml.ElementTree`
  ersetzt (3 Stellen in `core.py`, XML-Entity-/Billion-Laughs-Schutz beim
  Einlesen von DOCX-/XLSX-Daten); `defusedxml` als Pflichtabhängigkeit ergänzt.
  Bandit (`bandit -r anonymizer_modul -ll`) danach ohne Befunde.
- README um den Abschnitt „Rechtlicher Rahmen und Verantwortung" ergänzt:
  Pseudonymisierung ≠ Anonymisierung (DSGVO), § 203 StGB-Hinweis für
  Berufsgeheimnisträger, englische Kurzfassung.
- Realer NER-Qualitätstest mit `de_core_news_lg` gegen ausschließlich
  synthetische Namen durchgeführt (Ergebnis: `TODO.md`).
- Public-Metadaten vorbereitet: README-Kopfsatz, `pyproject.toml`-Beschreibung
  und `ellmos-module.json`-`visibility` (→ `public-candidate`) von der
  bisherigen "PRIVAT"-Kennzeichnung befreit; tatsächliche Veröffentlichung
  bleibt ein separater Freigabeschritt (/repo-publish-check, Operator).

## 0.2.0 — 2026-07-16

- Ordnerverarbeitung transaktional und fail-closed gemacht; nicht unterstützte
  Formate, Parserfehler, Symlinks und Pfadkollisionen veröffentlichen nichts.
- Schlüsselpfade gegen Traversal, Cloud-Sync und Symlinks geschützt;
  verschlüsselte Dateien atomar mit privaten Berechtigungen geschrieben und
  begrenzt gelesen.
- Alle gültigen E-Mail-Domains sowie erkannte Tabellen-/NER-Namen und
  Institutionen in die Profilbildung aufgenommen; fehlendes NER ist im
  Standardmodus ein harter Stop.
- DOCX-/XLSX-OOXML-Oberflächen erweitert und nach dem Speichern auf Restdaten
  geprüft; Discovery erfasst paketweit Texte und identitätstragende Attribute
  einschließlich Chart-/Drawing-Flächen; nicht verifizierte Medien werden
  standardmäßig abgelehnt.
- PDF-Metadaten, XML-Metadaten, Annotationen, Links, Formulare und Anhänge
  sowie Bookmarks und Page-Labels entfernt; bildhaltige PDFs ohne OCR abgelehnt;
  angeforderte Verschlüsselung fällt nicht mehr auf Klartext zurück.
- spaCy-Installationen ohne ladbares Modell und unplausibel große NER-Blöcke
  stoppen den Standard-Scan; E-Mail-Ersetzung ist casing-sicher.
- Windows-Junctions/Reparse-Points werden wie Symlinks abgelehnt; vollständige
  Zielbäume werden erst über eine gleichvolumige atomare Umbenennung publiziert.
- Legacy-DOC-Eingabe, Konvertierung und Ausgabe begrenzt.
- Reale CLI-Unterbefehle mit verdeckter Eingabe und belastbaren Exitcodes
  ergänzt.
- Dokumentation und tatsächliche foerderplaner-Verkabelung synchronisiert.

## 0.1.0 — 2026-06-27

- Standalone-Extraktion aus BACH v1.2.0 mit neutralisierten Laufzeitpfaden.
