---
name: anonymizer
version: "0.2.2"
type: standalone-module
standalone: true
visibility: private
provenance: "Extrahiert aus BACH hub/_services/document/anonymizer_service.py v1.2.0"
dependencies:
  required:
    - cryptography       # authentifizierte Fernet-Schlüsseldateien
  optional:
    - python-docx        # Word-Dokumente
    - PyMuPDF            # PDF-Schwärzung
    - pikepdf            # PDF-Verschlüsselung
    - openpyxl           # Excel
tags:
  - anonymisierung
  - datenschutz
  - pseudonymisierung
  - klienten
  - foerderplanung
  - privat
description: |
  PRIVAT — Standalone-Anonymizer für klientenbezogene Dokumente.
  Pseudonymisiert personenbezogene Daten (Namen, Geburtsdaten, Adressen, Telefon, E-Mail)
  konsistent über mehrere Dateien. Authentifizierte lokale Schlüsselspeicherung.
  Unterstützt Text, DOCX, PDF und XLSX mit fail-closed Medien- und Restdatenkontrollen.
  Vollständig ohne BACH lauffähig.
---

# Anonymizer — Skill

## Auslöser

| Situation | Aktion |
|---|---|
| Förderplandokumente anonymisieren | `DocumentAnonymizer.anonymize_folder()` |
| Einzelne Datei anonymisieren | `DocumentAnonymizer.anonymize_file()` |
| Anonymisiertes Dokument wiederherstellen | `DocumentDeanonymizer.deanonymize_file()` |
| Profil mit Tarnnamen erstellen | `DocumentAnonymizer.create_profile()` |
| Text auf sensible Daten prüfen | `DocumentAnonymizer.scan_text_for_sensitive_data()` |
| Schlüssel verschlüsselt speichern | `encrypt_key_file()` |
| Schlüssel laden | `decrypt_key_file()` |

## Minimales Beispiel (nach Paketinstallation)

```python
from anonymizer_modul import DocumentAnonymizer

anon = DocumentAnonymizer()
profile = anon.create_profile(
    real_name="Max Mustermann",
    geburtsdatum="15.03.2016",
)
success, count = anon.anonymize_file("bericht.txt", profile)
print(f"Ersetzt: {count} Vorkommen")
```

## Pfad-Konfiguration

```python
import os
# Schlüsselspeicher (außerhalb OneDrive!)
os.environ["ANONYMIZER_KEYS_DIR"] = r"C:\_Local_Anon\keys"
# Klienten-Ausgabe
os.environ["ANONYMIZER_HOME"] = r"C:\_Local_Anon\output"
```

## Datenschutz-Hinweise

- Schlüssel (`.schluessel.enc`) NIEMALS in OneDrive — lokaler Speicher unter `%LOCALAPPDATA%\anonymizer\keys`
- Kein echter Personenname in Code, Tests oder Commits
- `.gitignore` schließt `keys/`, `*.enc`, `*.db` aus
- `result.errors` ist ein harter Stop; bei Fehlern wird kein Zielbaum veröffentlicht
- Ohne spaCy/NER bricht der Standard-Scan ab; reduzierter Modus nur nach bewusster Prüfung
- Bild-/Medieninhalte werden ohne gesonderten OCR-Workflow abgelehnt

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.2.2 | 2026-07-23 | NER-Plausibilitätsfilter strukturell auf POS/Lemma umgestellt (Referenzlauf RUN2) |
| 0.2.1 | 2026-07-23 | defusedxml-Härtung (OOXML-Parsing), Git/CI/Legal-Gates für Public-Vorbereitung |
| 0.2.0 | 2026-07-16 | Privacy-/Security-Härtung, transaktionale Ausgabe, Format-Restdatenkontrollen, reale CLI |
| 0.1.0 | 2026-06-27 | Extraktion aus BACH hub v1.2.0; BACH-Pfadbezüge neutralisiert |
