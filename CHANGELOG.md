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
- **Template-Medien-Fix (foerderplaner-Referenzlauf, Fund A):** DOCX/XLSX mit
  eingebetteten Bildern (z. B. Briefkopf-Logo im Berichts-Template) blockierten
  bisher IMMER die Ver-/De-Anonymisierung (`_has_unverified_package_content`
  ohne Ausnahme). Neuer optionaler `trusted_template_path` (API + CLI
  `--trusted-template` + ENV `ANONYMIZER_TRUSTED_TEMPLATE`) lässt gezielt
  `word/media`/`xl/media`-Einträge passieren, deren SHA-256-Hash
  byte-identisch aus dem angegebenen Template stammt; jeder andere Medien-
  Eintrag sowie Embeddings/ActiveX/VBA/OLE bleiben unverändert gesperrt
  (fail-closed-Prinzip erhalten). `DocumentDeanonymizer.deanonymize_file`/
  `deanonymize_folder` geben den Parameter durch, statt intern immer mit
  Default-`DocumentAnonymizer()` zu arbeiten.
- **NER-Plausibilitätsfilter erweitert (foerderplaner-Referenzlauf, Fund B):**
  `de_core_news_lg` markierte generische Verwaltungs-/Berichtssubstantive
  ("Landkreis Lörrach", "Förderung", "Zusage", "Ablauf") fälschlich als
  Personennamen. `_looks_like_person_name()` prüft Gattungsbegriffe jetzt an
  JEDER Wortposition (nicht mehr nur bei Einzelwort-Treffern) gegen eine
  erweiterte Verwaltungs-/Einrichtungs-/Berichtsvokabular-Liste
  (`_NER_GENERIC_REPORT_NOUNS`); die Stoppwortliste für satzfragment-
  verdächtige Spans wurde um Reflexivpronomen und Modal-/Hilfsverben ergänzt.
  Echte synthetische Namen ("Kim", "Anna Muster") bleiben erkannt.

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
