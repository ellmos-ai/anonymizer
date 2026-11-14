# Security and Privacy Policy / Sicherheits- und Datenschutzrichtlinie

`anonymizer` (`anonymizer-modul`) processes sensitive local documents completely offline. Only the latest `0.3.x` release line (`0.3.1`) receives active security and privacy updates.

## Supported Versions / Unterstützte Versionen

| Version | Supported / Unterstützt | Notes / Hinweise |
|---|---|---|
| `0.3.x` (`0.3.1`) | :white_check_mark: Yes / Ja | Active MIT core with isolated `[pdf-redact]` AGPL boundary (Decision E08) |
| `< 0.3.0` | :x: No / Nein | Superseded; upgrade to `0.3.1` required |

---

## Reporting a Vulnerability (English)

If you discover a security or privacy boundary issue, please report it privately and responsibly:

1. **Do NOT open a public GitHub issue** for suspected vulnerabilities or data-leakage vectors.
2. **Submit a private report via [GitHub Security Advisories](https://github.com/ellmos-ai/anonymizer/security/advisories/new).**
3. **Strict Synthetic-Data Rule:** Reports must contain **exclusively synthetic examples**, affected versions, reproducible steps, and the expected security boundary. **Never** attach real client documents, plaintext identities, or `.schluessel.enc` keyfiles.

### Response & Remediation SLAs

- **INV-SLA-10 (48-Hour Acknowledgement & 30-Day Remediation SLA):** You will receive an initial acknowledgement within **48 hours** and a verified fix or mitigation for confirmed vulnerabilities within **30 calendar days**.
- **INV-SLA-09 (5-Business-Day Triage):** Technical reproduction, severity assessment, and remediation plan within **5 business days**.
- **Coordinated Disclosure:** Please allow the remediation window to complete before public disclosure.

### Hard Security & Privacy Boundaries

- **Zero Network Egress (`INV-LOCAL-01`):** All scanning, pseudonymization, and restoration operations run 100% locally offline without telemetry or external API calls.
- **All-or-Nothing Fail-Closed Publication (`INV-LOCAL-02`, `INV-LOCAL-10`):** Unsupported formats, parser errors, symlinks/reparse points, unverified embedded media, or residual identity traces immediately abort staging before any target directory is published.
- **Authenticated Key Encryption & Cloud-Sync Rejection (`INV-LOCAL-03`):** Keyfiles (`.schluessel.enc`) use Fernet authenticated encryption with PBKDF2-HMAC-SHA256 (`480,000` iterations, `>= 12`-character passphrase, atomic `0o600` file creation) and actively reject known cloud-synchronized paths (such as OneDrive, Dropbox, iCloud, Google Drive). Operators using custom sync folders must additionally choose a guaranteed local directory.
- **Hardened Parsers & Media Gate (`INV-LOCAL-07`):** OOXML archives (`.docx`, `.xlsx`) are parsed via `defusedxml` against XML entity expansion attacks; embedded media blocks publication unless matched byte-for-byte via SHA-256 against an explicit `--trusted-template`.
- **Fail-Closed NER:** Missing spaCy or language models abort standard scans rather than silently downgrading (`require_ner=False` requires explicit opt-in).
- **Zero-PII Diagnostics:** Logs, tests, and CLI error messages never emit real identities or sensitive source filenames.

---

## Sicherheitsmeldung & Datenschutzgrenzen (Deutsch)

Sicherheits- oder Datenschutzlücken bitte ausschließlich vertraulich melden:

1. **Kein öffentliches GitHub-Issue** für potenzielle Sicherheits- oder Datenschutzprobleme eröffnen.
2. **Vertrauliche Meldung über [GitHub Private Vulnerability Reporting](https://github.com/ellmos-ai/anonymizer/security/advisories/new) einreichen.**
3. **Strikte Synthetik-Regel:** Meldungen dürfen ausschließlich synthetische Beispiele, betroffene Versionen, reproduzierbare Schritte und die erwartete Schutzgrenze enthalten. **Niemals** echte Klientendaten, Originaldokumente oder `.schluessel.enc`-Schlüsseldateien anhängen.

### Verbindliche Reaktions- und Behebungsfristen (SLA)

- **INV-SLA-10 (48h Bestätigung & 30 Kalendertage Behebungszusage):** Eingangsbestätigung innerhalb von **48 Stunden**; Bereitstellung eines geprüften Patches oder Workarounds für bestätigte Sicherheitslücken innerhalb von **30 Kalendertagen**.
- **INV-SLA-09 (5 Werktage Triage):** Technische Reproduktion, Schweregradeinstufung und Maßnahmenplan innerhalb von **5 Werktagen**.

### Harte Schutzgrenzen

- Schlüsseldateien (`.schluessel.enc`, Fernet + PBKDF2-HMAC-SHA256 mit `480.000` Iterationen, Mindestlänge `12` Zeichen, atomare `0o600`-Ablage) und wiederhergestellter Klartext bleiben strikt außerhalb erkannter Cloud-Sync-Pfade. Benutzerdefinierte oder umbenannte Sync-Dienste müssen Betreiber zusätzlich durch eine garantiert lokale Pfadwahl ausschließen.
- Ein Parserfehler, Symlink/Reparse-Point oder nicht unterstützter Inhalt veröffentlicht niemals einen teilweise pseudonymisierten Zielbaum (`Fail-Closed`).
- Bild- und Medieninhalte gelten ohne separat validierten OCR-Pfad als nicht verifiziert und werden standardmäßig abgelehnt (Ausnahme: exakter SHA-256-Treffer gegen ein explizit übergebenes Referenztemplate `--trusted-template`).
- Fehlende NER-Abdeckung ist im Standardmodus ein harter Fehler, kein stilles Herabstufen.
- Logs, Tests und Fehlertexte enthalten keine echten Identitäten oder identifizierenden Quellpfade.

### Bekannte Grenzen / Known Limitations

- PDF-Inhaltsstrom-Schwärzung (`[pdf-redact]`, PyMuPDF / AGPL-3.0, isoliert gemäß Entscheidung E08) ist technisch irreversibel.
- Bildinhalte werden nicht per OCR pseudonymisiert und deshalb fail-closed abgelehnt.
- Die lokale Cloud-Pfadprüfung erkennt bekannte Anbieter und Windows-OneDrive-Umgebungswurzeln, aber keine beliebig benannten Drittanbieter-Synchronisationsordner.
- Pseudonymisierung nach Art. 4 Nr. 5 DSGVO ersetzt keine manuelle Endkontrolle vor einer Weitergabe durch Berufsgeheimnisträger (§ 203 StGB).
