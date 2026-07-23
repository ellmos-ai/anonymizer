# AGENTS.md — anonymizer-Modul

Weiterleitungsdatei für KI-Agenten. Kanonische Regeln stehen in README.md und SKILL.md.

## Rollen

| Rolle | Beschreibung |
|---|---|
| Anonymisierer | Erstellt Profile, anonymisiert Ordner/Dateien mit `DocumentAnonymizer` |
| De-Anonymisierer | Stellt Dokumente mit `DocumentDeanonymizer` + Schlüssel wieder her |
| Schlüsselverwalter | Verwaltet `.schluessel.enc`-Dateien im lokalen Schlüsselspeicher |

## Harte Regeln

- `PRIVAT` — keine Klienten-Klarnamen in Logs, Commits oder Protokollen.
- `keys/`-Ordner und `*.schluessel.enc`-Dateien NIEMALS committen oder in OneDrive ablegen.
- Vor dem Ausführen: prüfen ob eine aktive `LOCK*.txt` im Modulordner liegt.
- Keine echten Personennamen in Tests — nur fiktive Namen (Max Mustermann, Frau Schmidt).
- BACH-Imports (`bach_paths`, `from hub`, `from core`) NIEMALS hinzufügen.

## Änderungsregeln

- **Keine** Funktionalität ohne Rücksprache entfernen.
- **Keine** BACH-Bezüge einführen.
- **Immer** `py_compile` und Smoke-Test nach Änderungen an `core.py` laufen lassen.

Vollständige Dokumentation: README.md
