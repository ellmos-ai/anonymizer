# Third-Party Software Licenses and Dependencies

This document provides a comprehensive inventory of third-party software packages and libraries utilized by `anonymizer` (`anonymizer-modul`), along with their respective licensing conditions and governance boundaries.

## Primary Project License

`anonymizer` is licensed under the **MIT License**:

```text
MIT License

Copyright (c) 2026 ellmos / BACH Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Core Runtime Dependencies

These libraries are mandatory for the baseline operation of `anonymizer` (authenticated key encryption and secure XML parsing):

| Package | Minimum Version | License | Upstream Link | Purpose in `anonymizer` |
|---|---|---|---|---|
| `cryptography` | `>=41.0` | Apache-2.0 / BSD-3-Clause | [GitHub](https://github.com/pyca/cryptography) | Authenticated Fernet encryption with PBKDF2-HMAC-SHA256 key derivation for client keyfiles. |
| `defusedxml` | `>=0.7` | Python Software Foundation (PSF-2.0) | [GitHub](https://github.com/tiran/defusedxml) | Defensively parsing OOXML XML trees in DOCX and XLSX against billion-laughs and entity-expansion attacks. |

---

## Optional Format Extras (Permissive / AGPL-Free)

These dependencies can be installed selectively (`docx`, `pdf`, `excel`, `ner`) or together (`all`). All dependencies in this group are strictly AGPL-free and compatible with MIT distribution:

| Package | Extra | Minimum Version | License | Upstream Link | Purpose in `anonymizer` |
|---|---|---|---|---|---|
| `python-docx` | `docx`, `all` | `>=1.0` | MIT License | [GitHub](https://github.com/python-openxml/python-docx) | Word document structure parsing and paragraph/table pseudonymization. |
| `pypdf` | `pdf`, `all` | `>=4.0` | BSD-3-Clause | [GitHub](https://github.com/py-pdf/pypdf) | Read-only PDF text extraction for sensitive entity scanning without modifying PDF content. |
| `pikepdf` | `pdf`, `all` | `>=8.0` | Mozilla Public License 2.0 (MPL-2.0) | [GitHub](https://github.com/pikepdf/pikepdf) | PDF AES-256 password protection and encryption without modifying source streams. |
| `openpyxl` | `excel`, `all` | `>=3.1` | MIT License | [GitLab](https://foss.heptapod.net/openpyxl/openpyxl) | Excel spreadsheet parsing, comments sanitization, and sheet pseudonymization. |
| `spacy` | `ner`, `all` | `>=3.7` | MIT License | [GitHub](https://github.com/explosion/spaCy) | Named Entity Recognition (NER) for identifying personal names (`PER`) in running text. |

---

## Isolated PDF Content-Stream Redaction Extra (AGPL Boundary)

In accordance with **Architectural Decision E08** (2026-08-18), PyMuPDF is strictly quarantined in its own optional extra `pdf-redact`:

| Package | Extra | Minimum Version | License | Upstream Link | Boundary Notice |
|---|---|---|---|---|---|
| `PyMuPDF` (`fitz`) | `pdf-redact` | `>=1.22` | GNU Affero General Public License v3 (AGPL-3.0) | [PyPI](https://pypi.org/project/PyMuPDF/) | Required strictly for true in-stream vector text redaction in `_anonymize_pdf()`. Excluded from `all` and `pdf` extras. |

> [!IMPORTANT]
> PyMuPDF is licensed under AGPL-3.0. To protect downstream MIT distribution and bundling, `PyMuPDF` is NEVER included in default or `all` dependency sets. Users requiring deep vector redaction in PDFs must deliberately opt in via `pip install anonymizer-modul[pdf-redact]`.

---

## Development & Test Tooling

| Package | License | Purpose |
|---|---|---|
| `pytest` | MIT License | Test framework and contract test runner |
| `ruff` | MIT / Apache-2.0 | Fast static analysis, linting, and formatting |
| `bandit` | Apache-2.0 | Automated AST security and vulnerability linter |
| `build` | MIT License | PEP 517 build frontend |
| `twine` | Apache-2.0 | Distribution package validation and check utility |
