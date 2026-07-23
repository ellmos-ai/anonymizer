# Privacy-/Security-Review 2026-07-16

## Umfang und Ausgangspunkt

Geprüft wurde der vollständige private Modulordner als unveränderlicher
0.1.0-Snapshot mit der Kennung
`snapshot_20260716T1214_157ab255`. Der Ausgangs-Hash von
`anonymizer_modul/core.py` war
`c9077830fe93e1804c273a811661a0cae3b250619061f9f02f067e103dbc69c2`.
Die Prüfung umfasste Quelltext, Tests, Manifeste, Packaging, Schlüssel- und
Dateipfade sowie realistische synthetische Dokumente.

## Bestätigte Ausgangsbefunde

Der Baseline-Scan bestätigte 16 berichtspflichtige Datenschutz-/Security-
Befunde: sechs hohe, sechs mittlere und vier niedrige Prioritäten.

| Bereich | Ausgangsrisiko | Korrektur in 0.2.0 |
|---|---|---|
| DOCX/XLSX/PDF-Restflächen | Kommentare, Metadaten, Formulare, Anhänge oder Bilder konnten Identitäten behalten | OOXML-weite Textkontrolle, PDF-Bereinigung, Restdatenprüfung, Medien ohne OCR fail-closed |
| NER und Profilbildung | fehlendes NER sowie verworfene Tabellen-/NER-Namen führten zu unvollständigen Mappings | Standard-Scan bricht ohne NER ab; alle erkannten Namen/Institutionen werden gemappt |
| E-Mail-Erkennung | nur eine private Domainliste wurde übernommen; Großschreibung konnte die Ersetzung umgehen | jede syntaktisch gültige E-Mail-Adresse gilt als sensibel und wird casing-sicher ersetzt |
| Ordnerveröffentlichung | Rohkopien blieben bei nicht unterstützten Formaten oder Handlerfehlern zurück | Verarbeitung im lokalen Staging; Veröffentlichung nur bei vollständig grüner Prüfung |
| Pfade und Dateinamen | Quell-Symlinks/Junctions, identifizierende Verzeichnisnamen und Kollisionen | Reparse-/No-follow-Grenzen, alle relativen Komponenten pseudonymisiert, Kollisionen stoppen |
| Schlüsselablage | ENV-/Ausgabepfade konnten Cloud-Sync oder Traversal zulassen | strikte Client-ID, Cloud-/Symlink-Prüfung, atomare private Datei, Größenlimit |
| Legacy DOC | externe Konvertierung ohne Eingabe-/Ausgabegrößenlimit | 25-MiB-Eingabe-, 50-MiB-Ausgabe- und feste Timeout-Grenzen |
| Fehler und CLI | Quellnamen in Fehlern; angekündigte CLI-Befehle waren No-ops | opake Dateiindizes, echte Unterbefehle und nicht-null Exitcodes |

Zusätzliche niedrig priorisierte oder operatorlokale Kandidaten wurden im
Baseline-Scan geprüft. Relevante Sicherheitsgrenzen daraus (Client-ID,
Key-Dateigröße, Ziel-Symlinks, Quell-/Zielalias und PDF-Verschlüsselungsfehler)
sind ebenfalls mit Tests abgesichert.

## Verifikation

Die Schutztests verwenden ausschließlich fiktive Marker. Sie prüfen unter
anderem:

- DOCX-Kommentare und Kernmetadaten auf Paketebene,
- XLSX-Kommentare, versteckte Blätter, Dokumenteigenschaften und Charttitel,
- vollständige Scan→Profil→Publish-Pfade über alle OOXML-Teile und textuellen
  Attribute,
- PDF-Text, Metadaten, Annotationen, Anhänge, Bookmarks und Page-Labels,
- Medien-Stopps mit unverändertem Original,
- Formatfehler ohne veröffentlichten Zielordner,
- Cloud-/Traversal-/Alias-/Dateinamen-Grenzen,
- NER-Fail-closed bei fehlender Bibliothek, fehlenden Modellen und unplausibel
  großen Trefferblöcken sowie vollständige Profilbildung,
- Windows-Reparse-Points und gleichvolumige atomare Zielbaum-Veröffentlichung,
- CLI-Selbsttest und Fehlerexit.

Auf diesem Windows-Host konnten Tests, die das Erstellen symbolischer Links
erfordern, mangels Betriebssystemprivileg übersprungen werden. Die
No-follow-Pfade wurden zusätzlich statisch nachverfolgt; echte Symlink-
Laufzeitprüfung bleibt für eine privilegierte oder Unix-artige CI offen.

Die endgültigen Befehle und Ergebnisse stehen in `RELEASE_GATE.md`.

## Ergebnis und verbleibende Grenzen

Der frische unabhängige Schlussreview fand zunächst drei P1 und drei
release-relevante P2 in den Modell-, OOXML-, E-Mail-, PDF-, Junction- und
Veröffentlichungsgrenzen. Nach den gezielten Fix-/Nachcheck-Runden endete die
unabhängige Zählung mit **0×P0/P1/release-relevante P2**. Die vollständige
Suite umfasst 54 bestandene Tests plus drei bestandene Subtests; zwei echte
Symlink-Fixtures bleiben ausschließlich wegen Windows-Rechten übersprungen.

Die bestätigten Produktpfade sind in 0.2.0 geschlossen und durch
Regressionstests abgedeckt. Das Modul bleibt dennoch ein privater
Entwicklungsstand: OCR fehlt, reale NER-Modelle wurden auf diesem Host nicht
installiert, und es gibt keinen Git-/CI-/Signaturkontext. Bildhaltige Eingaben
werden deshalb standardmäßig abgelehnt; Public Release bleibt gesperrt.
