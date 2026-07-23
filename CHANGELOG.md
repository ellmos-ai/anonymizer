# Changelog

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
