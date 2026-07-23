# Release Gate — anonymizer 0.2.0

Stand: 2026-07-16

## Entscheidung

**Private development use: bedingt freigegeben. Public Release: gesperrt.**

Die Datenschutzgrenzen sind lokal verifiziert. Der unabhängige Ausgangsreview
fand 3×P1 und 3×release-relevante P2; die gezielten Nachchecks endeten mit
**0×P0/P1/release-relevante P2**. Ein öffentlicher Release ist wegen fehlendem
Git-/CI-/Signaturkontext, nicht installiertem realem NER-Modelltest und
fehlendem OCR-Workflow weiterhin nicht zulässig.

## Prüfgates

| Gate | Ergebnis |
|---|---|
| Syntax/Import | grün — `py_compile` für Core und Schutztests |
| Vollständige Testsuite | grün — 54 bestanden, 2 OS-Skips, 3 Subtests bestanden |
| Schutz-PoCs / alternative Eingaben | grün — 31 Schutztests: OOXML-Attribute/Charts, NER, Casing, PDF-TOC, Reparse und atomare Veröffentlichung |
| CLI | grün — UTF-8-Selbsttest und installierte Wheel-Hilfe mit echten Unterbefehlen |
| Build und Archivinhalt | grün — isolierter sdist-/Wheel-Bau; keine Locks, Backups, Caches oder Bytecode im Wheel |
| Paketprüfung | grün — frische Wheel-Installation 0.2.0 und `pip check`; Twine auf diesem Host nicht installiert |
| Modulmanifeste | grün — gültiges JSON, Katalog aktuell mit 38 Modulen, 11 Katalogtests und Beispielkomposition grün |
| Unabhängiger Schlussreview | grün — 0×P0/P1/release-relevante P2 |
| Öffentlicher Sammel-Gate | erwarteter Stop — Modulordner ist kein Git-Repository |

## Bekannte Restpunkte

- Zwei Symlink-Laufzeittests benötigen Windows-Entwicklermodus/Adminrechte
  oder einen Unix-CI-Runner; Reparse-/Junction-Erkennung ist zusätzlich
  deterministisch getestet.
- Reale spaCy-Modelle und OCR sind nicht Teil dieses lokalen Gates.
- Der Modulordner ist kein Git-Repository; Commit und Push sind nicht möglich.
- Bandit, Twine, Signierung und Mehrplattform-CI stehen lokal nicht zur
  Verfügung und bleiben öffentliche Release-Gates.
