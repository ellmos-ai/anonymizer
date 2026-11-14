# TODO — anonymizer

## STATUS

| Category | Status | Notes |
|----------|--------|-------|
| Secrets | :green_circle: OK | 0 Secrets in getrackten Dateien; API-Beispiele nutzen Umgebungsvariablen (`ANONYMIZER_PASSPHRASE`), Tests kanonische Sentinels |
| Private Data (PII) | :green_circle: OK | 0 echte Klientendaten oder Entwickler-PII; ausschließlich synthetische Referenzidentitäten (`Max Mustermann`, `Frau Schmidt`) |
| Hardcoded Paths | :green_circle: OK | 0 persönliche Entwicklerpfade; Cloud-Sync-Verzeichnisse werden für Schlüssel und Klartext aktiv abgewiesen |
| Database Files | :green_circle: OK | 0 `.db`-, `.sqlite`- oder `.schluessel.enc`-Dateien getrackt |
| .env Files | :green_circle: OK | 0 `.env`-Dateien getrackt; `.gitignore` schützt Umgebungsvariablen, Schlüssel, Zertifikate und Tokens |
| BACH Internals | :green_circle: OK | 0 interne Altdateien oder Laufzeit-Imports; 100 % eigenständiges Standalone-Modul |
| .gitignore | :green_circle: OK | Alle Release-Gate-Pflichtmuster (`__pycache__`, `*.pyc`, `.env`, `*.db`, `.venv/`, `.idea/`, `.vscode/`, `data/`), Keys, Locks und Flotten-Tokens verankert |
| Language & Parity | :green_circle: OK | Englisches `README.md` + deutsches `README_de.md` mit 12-teiliger Navigationsparität, Mermaid-Diagrammen und echten UTF-8-Umlauten |
| LICENSE & SBOM | :green_circle: OK | MIT-Lizenz, Level 1 SBOM (`THIRD_PARTY_LICENSES.md`), AGPL-Isolation in `[pdf-redact]` (`tests/test_no_agpl.py`), Dependabot aktiv |
| Overall | **PASS (10/10 Gates)** | `final_gate_check.py` 10 PASS, 0 FAIL, 0 WARN (`READY FOR PUBLIC RELEASE`); Pytest & Ruff 100 % grün |

**Audit-Datum:** 2026-11-14 (`[AI_SECURITY_AND_DEPENDENCY_AUDIT]`)<br>
**Gate-Check-Ergebnis:** 10 PASS, 0 FAIL, 0 WARN (`READY FOR PUBLIC RELEASE`)<br>
**Rolle:** Fail-Closed Standalone-Dienst für lokale Dokument-Pseudonymisierung (`privacy.anonymize`, `privacy.pseudonymize`)<br>
**Stand:** 2026-11-14 · Version `0.3.1` (eingefroren)

## Offen

- [ ] **Kontrollierter OCR-Vorstufen-Vertrag:** Separaten, explizit freizugebenden OCR-Workflow definieren, bevor bildhaltige DOCX-, XLSX- oder PDF-Dokumente außerhalb von SHA-256-verifizierten Briefkopf-Templates (`--trusted-template`) verarbeitet werden dürfen (aktuell bewusst fail-closed).
- [ ] **Lokaler DLP-Companion-Adaptervertrag:** Schnittstellenvertrag für optionale lokale Prompt-/DLP-Gateways definieren, ohne `anonymizer` selbst in einen Netzwerkproxy zu verwandeln (strikte Isolation der `.schluessel.enc`-Schlüsseldateien von Netzwerkprozessen).
- [ ] **Optionale PyPI-Paketveröffentlichung:** Bei künftiger Operator-Freigabe Paketpublikation von `anonymizer-modul` auf PyPI sowie korrespondierende Release-Tags prüfen.

## Bewusst nicht gebaut

- **Ausgehende Netzwerk- oder Cloud-Anbindung** — Alle Scan-, Pseudonymisierungs- und De-Pseudonymisierungsschritte laufen ausnahmslos lokal und offline (`INV-LOCAL-01`).
- **Stille Fallback-Modi bei Parser- oder Medienfehlern** — Nicht verifizierbare Medien, beschädigte Archive oder fehlende NER-Modelle stoppen die Veröffentlichung im Standardmodus vollständig (`INV-LOCAL-02`).
- **Implizite AGPL-Abhängigkeit im Standard-Bundle** — `PyMuPDF` bleibt gemäß Entscheidung E08 strikt auf das explizite Extra `[pdf-redact]` begrenzt (`INV-LOCAL-08`).

## Abgeschlossene Aufgaben

- [x] **TASK-ANON-SEC-01 (2026-11-14): AI Security, Privacy & Dependency Audit (`v0.3.1`)**
  - **Ergebnis:** `final_gate_check.py` von `7 PASS / 3 FAIL` auf **10 PASS / 0 FAIL / 0 WARN** gehärtet: `.gitignore` um Release-Gate-Pflichtmuster (`*.pyc`, `.env`, `data/`), Zertifikats-/SSH-/Token-Exklusionen und SQLite-Dateien erweitert; literale Passphrasen in `README.md`, `README_de.md` und `llms.txt` auf `os.environ["ANONYMIZER_PASSPHRASE"]` sowie Test-Fixture in `tests/test_security_boundaries.py` auf Sentinel `"CHANGE-ME-IN-PRODUCTION"` umgestellt; `SECURITY.md` zweisprachig (EN/DE) auf `v0.3.1`, GitHub Security Advisories und verbindliche 48h/5d/30d-SLAs (`INV-SLA-09`, `INV-SLA-10`) aktualisiert; `.github/dependabot.yml` (`pip` & `github-actions`), Level-1-SBOM (`THIRD_PARTY_LICENSES.md`), `SKILL.md` und `TODO.md` synchronisiert; 4 neue Sicherheits- und Governance-Vertragstests in `tests/test_metadata.py` ergänzt.
- [x] **2026-11-05: CI-Matrix-Härtung (Python 3.10–3.12, `pip check`, `build`-Job), PEP 561 `py.typed` & `MANIFEST.in`-Vollständigkeit.**
- [x] **2026-09-19: PEP 621 Standardisierung (`0.3.1`), Least-Privilege CI-Permissions, Level 1 SBOM & § 521 BGB Haftungsausschluss.**
- [x] **2026-08-18: Entscheidung E08 — Isolierung der AGPL-3.0-Abhängigkeit `PyMuPDF` im separaten Extra `[pdf-redact]` (`0.3.0`).**
