# anonymizer — Standalone-Modul

`anonymizer` 0.2.1 pseudonymisiert lokale Dokumente ohne BACH-Laufzeitimport.
Das Modul verarbeitet sensible personenbezogene Daten ausschließlich lokal;
Verantwortung, Grenzen und rechtlicher Rahmen der Nutzung stehen unter
„Rechtlicher Rahmen und Verantwortung" weiter unten.

## Sicherheitsvertrag

- `anonymize_folder()` veröffentlicht entweder einen vollständig geprüften
  Zielbaum oder gar keinen. Nicht unterstützte Dateien, Parserfehler,
  symbolische Links, Kollisionen und Restdaten stoppen die Veröffentlichung.
- Relative Ordner- und Dateinamen werden pseudonymisiert. Die Einzeldatei-API
  verweigert identifizierende Dateinamen, weil ihr Rückgabewert keinen neuen
  Pfad transportiert; für solche Eingaben ist der Ordner-Workflow vorgesehen.
- Schlüsseldateien werden mit Fernet authentifiziert verschlüsselt; der
  Schlüssel wird per PBKDF2-HMAC-SHA256 aus einem Passwort abgeleitet. Ablage
  und ENV-Override in bekannten Cloud-Sync-Pfaden werden abgelehnt.
- De-anonymisierte Klartextordner dürfen nicht in bekannte Cloud-Sync-Pfade
  geschrieben werden.
- Die automatische Personennamenerkennung arbeitet standardmäßig fail-closed:
  fehlen spaCy oder die konfigurierten Modelle, bricht der Scan ab. Ein
  reduzierter Modus muss explizit mit `require_ner=False` gewählt werden.

## Unterstützte Formate

| Format | Verhalten |
|---|---|
| `.txt`, `.md` | wortgrenzensichere Ersetzung |
| `.docx` | Absätze, Tabellen und paketweite OOXML-Texte/-Attribute einschließlich Kopf-/Fußzeilen, Kommentare, Diagramme und Metadaten |
| `.xlsx` | Zellen, Datumswerte und paketweite OOXML-Texte/-Attribute einschließlich Kommentare, Charttitel, Links, Blatt- und Dokumentmetadaten |
| `.pdf` | Textschwärzung; Metadaten, Annotationen, Formulare, Links, Anhänge, Bookmarks und Page-Labels werden entfernt |
| `.doc` | begrenzte externe Textextraktion; sichere Ausgabe als `.txt` |

Bild- oder eingebettete Binärinhalte in DOCX/XLSX und bildhaltige PDFs werden
standardmäßig abgelehnt, weil das Modul keine OCR-Garantie geben kann.
`allow_unverified_media=True` ist nur für einen separat geprüften lokalen
Workflow vorgesehen und darf nicht als vollständige Anonymisierung gelten.

Ordner werden zunächst vollständig in einer lokalen Arbeitsfläche geprüft.
Der fertige Zielbaum wird anschließend über einen gleichvolumigen
Geschwisterpfad in einer atomaren Umbenennung sichtbar; Kopier- oder
Umbenennungsfehler veröffentlichen keinen Teilbaum.

PDF-Schwärzung ist nicht reversibel. `DocumentDeanonymizer` kopiert bereits
geschwärzte PDFs lediglich weiter; eine vollständige Wiederherstellung wird
nicht versprochen.

## Rechtlicher Rahmen und Verantwortung

`anonymizer` **pseudonymisiert** Dokumente — es anonymisiert im
datenschutzrechtlichen Sinn nicht. Nach Art. 4 Nr. 5 DSGVO ersetzt
Pseudonymisierung identifizierende Merkmale durch ein Pseudonym, ohne den
Personenbezug technisch endgültig aufzuheben: Die verschlüsselte
Zuordnungstabelle (siehe „Sicherheitsvertrag") macht eine Re-Identifizierung
durch den Verwender bewusst möglich (`DocumentDeanonymizer`). Die
verarbeiteten Dokumente bleiben deshalb personenbezogene Daten im Sinne der
DSGVO, und die Verantwortung für Rechtsgrundlage, Zweckbindung,
Speicherbegrenzung und technisch-organisatorische Maßnahmen (Art. 5, 6, 24,
32 DSGVO) verbleibt vollständig beim Verwender des Moduls. Das Modul liefert
eine technische Schutzmaßnahme, keine rechtliche Bewertung und keine Garantie
für einen bestimmten DSGVO-Compliance-Status.

Für **Berufsgeheimnisträger** (§ 203 StGB, z. B. Ärzt:innen,
Psychotherapeut:innen, Rechtsanwält:innen, Sozialarbeiter:innen) gilt
zusätzlich: Der Einsatz von `anonymizer` entbindet nicht von den
berufsrechtlichen Schweigepflichten. Insbesondere bleibt die Weitergabe
pseudonymisierter Dokumente an Dritte (einschließlich Cloud-Dienste,
KI-Anbieter oder sonstige Auftragsverarbeiter) eigenverantwortlich zu prüfen.
Das Modul gibt — wie unter „Unterstützte Formate" und in `SECURITY.md`
dokumentiert — **keine Garantie**, dass sämtliche personenbezogenen Daten
vollständig erkannt und entfernt werden: Die Personennamenerkennung (NER) ist
modellbasiert und fehleranfällig, bildhaltige Inhalte werden ohne
OCR-Prüfung standardmäßig abgelehnt, und nicht unterstützte Formate werden
nicht verarbeitet. Vor jeder Weitergabe ist eine manuelle Endkontrolle durch
den Verwender erforderlich.

**Legal note (English summary):** `anonymizer` performs pseudonymization, not
GDPR-grade anonymization — identifying data is replaced by a reversible
pseudonym (Art. 4(5) GDPR), and the encrypted key file allows
re-identification by design. Processed documents remain personal data under
GDPR; legal basis, purpose limitation, and technical/organizational measures
(Art. 5, 6, 24, 32 GDPR) remain the sole responsibility of the operator. For
professionals bound by statutory confidentiality duties (e.g., doctors,
therapists, lawyers — cf. German § 203 StGB and equivalent regimes
elsewhere), using this module does not discharge those duties, and sharing
pseudonymized output with third parties (including cloud or AI providers)
must be assessed independently. The module gives **no guarantee** that all
personal data is detected and removed — NER is model-based and fallible,
image content is rejected by default without OCR verification, and
unsupported formats are not processed. A manual final review before
disclosure is required.

## Installation

Virtuelle Umgebungen und Schlüssel gehören außerhalb von OneDrive:

```powershell
py -m venv C:\_Local_Anon\venv
C:\_Local_Anon\venv\Scripts\python -m pip install -e "C:\Pfad\zu\anonymizer[all]"
```

`cryptography` ist Pflichtabhängigkeit. Format-Extras können gezielt als
`docx`, `pdf`, `excel` oder gemeinsam als `all` installiert werden. Die
spaCy-Modelle werden separat installiert:

```powershell
python -m spacy download de_core_news_lg
python -m spacy download en_core_web_lg
```

## Python-API

Das sichere Nutzungsmuster scannt zuerst, erstellt aus allen Treffern ein
Profil und veröffentlicht anschließend in einen neuen/leeren Zielpfad:

```python
import os
from anonymizer_modul import DocumentAnonymizer

os.environ["ANONYMIZER_KEYS_DIR"] = r"C:\_Local_Anon\keys"

anonymizer = DocumentAnonymizer()
scanned = anonymizer.scan_folder_for_sensitive_data(r"C:\Eingang\Fallakte")
profile = anonymizer.create_profile(
    real_name="Max Mustermann",       # ausschließlich fiktives Beispiel
    geburtsdatum="15.03.2016",
    scanned_data=scanned,
)
result = anonymizer.anonymize_folder(
    folder=r"C:\Eingang\Fallakte",
    profile=profile,
    password="ein-langes-lokales-passwort",
    output_folder=r"C:\Ausgang\K_ABC123",
)
if result.errors:
    raise RuntimeError("Anonymisierung wurde nicht veröffentlicht")
```

Fehlermeldungen und Fortschrittsdaten verwenden absichtlich nur opake
Dateiindizes. Sie enthalten keine Quellnamen oder absoluten Pfade.

## CLI

Passwörter, Name und Geburtsdatum werden verborgen abgefragt und erscheinen
nicht in Prozessargumenten:

```powershell
anonymizer self-test
anonymizer anonymize C:\Eingang\Fallakte C:\Ausgang\K_ABC123
anonymizer deanonymize C:\Ausgang\K_ABC123 C:\_Local_Anon\keys\K_ABC123.schluessel.enc C:\_Local_Anon\Wiederhergestellt
```

Der installierte Entry-Point und `python -m anonymizer_modul.core` verwenden
dieselben Befehle und liefern bei ungültigen Kommandos einen Exitcode ungleich
null.

## Tests und Status

```powershell
python -m py_compile anonymizer_modul\core.py
python -m pytest -q
python -m anonymizer_modul.core self-test
```

Der aktuelle Prüfstand steht in `RELEASE_GATE.md`; die detaillierte
Datenschutzprüfung in `SECURITY_REVIEW_2026-07-16.md`.

## Integration

Der aktuell nachgewiesene Konsument ist der foerderplaner-Skill mit einem
Reexport-Shim. Es gibt in diesem Checkout keine angebundene `FoerderDB`.
Die exakten Pfade und Verantwortungsgrenzen stehen in `WIRING.md`.

Lizenz: MIT. Herkunft: aus BACH
`hub/_services/document/anonymizer_service.py` v1.2.0 extrahiert und als
Standalone-Modul neutralisiert.
