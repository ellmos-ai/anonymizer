# Security and privacy policy

`anonymizer` verarbeitet besonders schützenswerte lokale Daten. Version 0.2.1
ist der einzige aktuell gewartete Stand.

## Meldung

Sicherheits- oder Datenschutzprobleme werden lokal an den Modulverantwortlichen
gemeldet. Berichte dürfen ausschließlich synthetische Beispiele, betroffene
Versionen, reproduzierbare Schritte und die erwartete Schutzgrenze enthalten.
Keine echten Klientendaten, Schlüsseldateien oder Originaldokumente anhängen.

## Harte Grenzen

- Schlüsseldateien und wiederhergestellter Klartext bleiben außerhalb der
  erkannten Cloud-Sync-Pfade. Benutzerdefinierte oder umbenannte Sync-Dienste
  müssen Betreiber zusätzlich durch eine garantiert lokale Pfadwahl ausschließen.
- Ein Fehler oder nicht unterstützter Inhalt darf keinen teilweise
  anonymisierten Zielbaum veröffentlichen.
- Bild-/Medieninhalte gelten ohne separat validierten OCR-Pfad als nicht
  verifiziert und werden standardmäßig abgelehnt.
- Fehlende NER-Abdeckung ist im Standardmodus ein Fehler, kein stilles
  Herabstufen.
- Logs, Tests und Fehlertexte enthalten keine echten Identitäten oder
  Quellpfade.

## Bekannte Grenzen

- PDF-Schwärzung ist irreversibel.
- Bildinhalte werden nicht per OCR anonymisiert.
- Der Ordner ist kein eigenes Git-Repository; Commit-Signaturen, Branch-Schutz
  und öffentliche Release-Artefakte sind daher nicht verfügbar.
- Die lokale Cloud-Pfadprüfung erkennt bekannte Anbieter und die Windows-
  OneDrive-Umgebungswurzeln, aber keine beliebig benannten Drittanbieter-Syncs.
