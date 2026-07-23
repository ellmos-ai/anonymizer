# WIRING — tatsächliche foerderplaner-Anbindung

Stand: 2026-07-16

## Nachgewiesener Verbraucher

Der aktuelle Checkout enthält genau eine direkte Integration:

```text
.AI/.MODULES/.DOMAINS/anonymizer/anonymizer_modul/core.py
        │
        ▼ Reexport
.AI/.SKILLS/skills/education/foerderplaner/
  scripts/services/anonymizer_service.py
        │
        ▼ Nutzung
  scripts/services/document_pipeline.py
```

Der Shim stellt die Modul-API für den Skill bereit. `document_pipeline.py`
verwendet unter anderem Mapping-, Extraktions-, Scan- und
Anonymisierungsabläufe. In diesem Checkout existieren weder eine verdrahtete
`FoerderDB` noch die früher genannten Dateien `report_workflow_service.py` oder
`foerderbericht_pipeline.py`. Solche Komponenten dürfen nicht als Ist-Zustand
dokumentiert oder importiert werden.

## Verantwortungsgrenze

1. Der Konsument übergibt ausschließlich explizit ausgewählte lokale
   Quelldateien bzw. einen Quellordner.
2. `anonymizer` scannt den Inhalt. Ohne spaCy/NER bricht der Standardmodus ab;
   ein reduzierter Modus braucht eine bewusste Entscheidung des Konsumenten.
3. Alle erkannten E-Mails, Institutionen, Tabellen- und NER-Personennamen
   fließen in `AnonymProfile.mappings` ein.
4. `anonymize_folder()` veröffentlicht erst nach erfolgreicher Verarbeitung
   aller sichtbaren Dateien. Bei Fehlern darf der Konsument keinen Zielbaum
   erwarten oder weiterreichen.
5. Die verschlüsselte Mapping-Datei verbleibt im lokalen
   `ANONYMIZER_KEYS_DIR`; sie wird nicht an den foerderplaner-Skill übergeben.

## Kompatibilitätsanforderungen für den Konsumenten

- `result.errors` muss als harter Stop behandelt werden.
- Nicht unterstützte Dateien und Medieninhalte müssen vorab getrennt oder über
  einen separat geprüften OCR-Pfad behandelt werden.
- Der Zielordner muss neu oder leer und außerhalb des Quellbaums sein.
- Der Konsument darf Quellnamen nicht selbst in Logs, Fehlertexte oder
  Telemetrie schreiben; das Modul liefert absichtlich opake Dateiindizes.
- Eine De-anonymisierung erzeugt Klartext und darf nur in einen lokalen,
  nicht cloud-synchronisierten Zielpfad erfolgen.

## Beispiel: direkte Modulnutzung

```python
from anonymizer_modul import DocumentAnonymizer

anonymizer = DocumentAnonymizer()
scan = anonymizer.scan_files_for_sensitive_data(selected_paths)
profile = anonymizer.create_profile(
    real_name=fictional_or_secure_input_name,
    geburtsdatum=secure_input_birth_date,
    scanned_data=scan,
)
result = anonymizer.anonymize_folder(
    folder=source_folder,
    profile=profile,
    password=secret_from_prompt,
    output_folder=fresh_output_folder,
)
if result.errors:
    raise RuntimeError("Anonymisierung nicht veröffentlicht")
```

Das Beispiel zeigt den Vertrag, nicht die interne Implementierung des
foerderplaner-Skills. Änderungen am Konsumenten gehören in einen eigenen Lauf
mit dessen Lock, Tests und Dokumentations-Writeback.
