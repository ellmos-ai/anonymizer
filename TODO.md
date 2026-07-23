# TODO — anonymizer

Stand: 2026-07-23, Version 0.2.4

## Status

| Bereich | Status | Beleg |
|---|---|---|
| Standalone-Import | grün | Keine BACH-Laufzeitimports; Smoke-Test vorhanden |
| Datenschutzgrenze | grün mit dokumentierten Limits | `tests/test_security_boundaries.py`, `SECURITY_REVIEW_2026-07-16.md` |
| Schlüsselablage | grün | Cloud-/Traversal-/Symlink-Grenzen und atomare verschlüsselte Ablage |
| Formate | grün, fail-closed | DOCX/XLSX/PDF-Restdaten- und Medienkontrollen |
| CLI | grün | echte Unterbefehle, verdeckte Geheimnisse, belastbare Exitcodes |
| Public Release | Tech-Gates erfüllt, Freigabe ausstehend | Git+CI+Bandit+Legal-Text+NER-Realtest grün (RELEASE_GATE.md); Metadaten (`visibility`, Beschreibungen) auf `public-candidate` umgestellt; offen: `/repo-publish-check` + tatsächliche Operator-Freigabe/Push |

## Public-Fahrplan (User-Entscheidung 2026-07-23: veröffentlichen nach
worksheet-generator + Berichts-Kern)

- [x] 2026-07-23: Git-Repo initialisiert (Branch `main`, Initial-Commit
  `2ef2e11`), `.github/workflows/ci.yml` angelegt (Python 3.11/3.12-Matrix
  auf `ubuntu-latest` löst die 2 Windows-Symlink-Skips; Lint-Job mit
  ruff + py_compile-Fallback; Bandit-Job `bandit -r anonymizer_modul -ll`).
  Twine bleibt manueller Schritt vor dem eigentlichen PyPI-Release, kein
  CI-Job. Kein Remote/Push — macht der Operator.
- [x] 2026-07-23: Realer NER-Modelltest mit `de_core_news_lg` (spaCy 3.8.14)
  gegen 10 ausschließlich synthetische Namen (Testperson Beispielmann u. a.)
  in einem sozialpädagogischen Beispieltext: **7/10 Nachnamen erkannt**
  (`Anke Testlehrer`, `Beispielmann`, `Erika Musterfrau`, `Finn
  Beispielkind`, `Johann Mustermann`, `Klaus Erfundenmann`, `Thomas
  Musterleiter`). Nicht erkannt: `Fallbeispiel` (nur Vorname „Petra"
  erfasst), `Testfall` (Titel „Dr." vor dem Namen störte offenbar die
  Erkennung), `Testkind`. Modell lädt und arbeitet korrekt; Erkennungsrate
  ist modelltypisch nicht vollständig — bestätigt die bestehende
  „keine Garantie vollständiger Erkennung"-Formulierung in README/SECURITY.
  `en_core_web_lg` wurde in diesem Lauf nicht installiert (nicht angefordert,
  ~500 MB zusätzlich); NER_MODELS bleibt für beide Sprachen konfiguriert.
- [x] 2026-07-23: README-Ergänzung „Rechtlicher Rahmen und Verantwortung":
  Pseudonymisierung ≠ Anonymisierung (Art. 4 Nr. 5, 5, 6, 24, 32 DSGVO),
  § 203 StGB-Hinweis für Berufsgeheimnisträger, englische Kurzfassung
  („Legal note (English summary)") am Abschnittsende.
- [x] 2026-07-23: Bandit-Blocker behoben (siehe „Offen" → jetzt „Erledigt")
  und Public-Metadaten umgestellt: README-Kopfsatz neutralisiert,
  `pyproject.toml`-Description ohne `PRIVAT:`-Präfix, `ellmos-module.json`
  `visibility` → `public-candidate`, Version 0.2.0 → 0.2.1 überall
  nachgezogen (siehe CHANGELOG.md).
- [ ] Release-Gates via /repo-publish-check → tatsächliche Operator-Freigabe
  → Push/Public (MIT). Reiner Metadaten-/Tech-Stand ist grün; Öffentlich-
  Stellung selbst bleibt bewusst ein separater, vom Operator zu treffender
  Schritt.

## Offen

- [ ] Den realen foerderplaner-Konsumenten in einem separaten, gelockten Lauf
  gegen den strikten NER-/Medienvertrag integrieren und dessen eigene veraltete
  Dokumentation bereinigen. Der bisherige Referenzlauf deckte zwei reale
  Defekte auf (Template-Medien-Blocker, NER-Overblocking) — siehe „Erledigt"
  2026-07-23 —, ein erneuter Referenzlauf gegen den gefixten Stand steht noch
  aus (geplant als Folge-Rerun).
- [ ] Einen kontrollierten OCR-Workflow definieren, bevor bildhaltige
  DOCX/XLSX/PDF-Dateien als anonymisierbar gelten dürfen.
- [ ] Optional: NER-Test zusätzlich mit `en_core_web_lg` wiederholen (in
  diesem Lauf nicht installiert, siehe Public-Fahrplan).
- [x] 2026-07-23: Git-Entscheidung getroffen — eigenes Repo (Branch `main`)
  im Modulordner selbst initialisiert statt separatem Privatbereich.
- [x] 2026-07-23: **Ehemaliger CI-Blocker behoben** (Operator-Entscheid: kein
  `# nosec`, gehärteter Parser ist Pflicht — Anonymizer verarbeitet per
  Definition unvertrauenswürdige Dokumente). `xml.etree.ElementTree` durch
  `defusedxml.ElementTree` ersetzt (Import in `core.py:57`; betraf die 3
  Aufrufstellen `core.py:592/631/668` — keine weiteren `ET.parse`/
  `fromstring`/`iterparse`-Stellen im Paket gefunden). `defusedxml>=0.7` als
  Pflichtabhängigkeit in `pyproject.toml` und `ellmos-module.json`
  `required_dependencies` ergänzt. `bandit -r anonymizer_modul -ll`: 0
  Medium/High (vorher 3× Medium/B314). Volle Testsuite danach erneut grün
  (54 passed, 2 skipped, 3 subtests).

## Erledigt

- [x] 2026-07-23: **RUN4-Feinschliff — Mehrwort-Span-Härtung (0.2.4):** Das
  0.2.3-Anker-Prinzip griff für Einzelwort-Spans, aber Mehrwort-Spans
  umgingen es: "Beim Anziehen"/"Beim Essen" (substantivierte Verben) und
  "Landkreises Lörrach" (Genitiv, Gattungsbegriff+Eigenname im selben
  Span) wurden über die "≥2 Tokens = verifiziert"-Regel trotzdem ersetzt.
  `_is_name_token()` prüft bei PROPN-Tokens jetzt zusätzlich das LEMMA:
  Gattungsbegriff-Lemma ("Landkreis") oder kleingeschriebenes Lemma
  (substantivierte Verben behalten ihr Infinitiv-Lemma, "Anziehen" →
  "anziehen") → Token wird aus dem Span gekürzt, bevor die Mehrwort-/
  Anker-Logik greift. DoD verifiziert: pytest mit geladenem
  `de_core_news_lg` — 65 passed, 2 skipped (beide Windows-Symlink-OS,
  kein Modell-Test übersprungen), 14 subtests. End-to-End gegen die echte
  RUN2-Akte: Profil-Mapping exakt {Kim, Beispiel, Kim Beispiel,
  Test-Fiktiv, Test-Mustermann, Sachbearbeiter-Fiktiv}. Neue Tests:
  `test_multiword_span_trims_generic_lemma_before_acceptance`,
  `test_multiword_span_trims_substantivized_verb_before_acceptance`
  (`tests/test_security_boundaries.py`); Positivfall "Anna
  Muster-Bergmann" (Bindestrich-Doppelname) ergänzt in
  `test_ner_run2_regression_positive_names_still_detected`.
- [x] 2026-07-23: **Referenzlauf-Fund A behoben (Template-Medien-Blocker):**
  DOCX/XLSX-Vorlagen mit eingebetteten Bildern (Briefkopf/Logo) ließen sich
  nie de-anonymisieren, weil `DocumentDeanonymizer.deanonymize_file` intern
  immer `DocumentAnonymizer()` mit `allow_unverified_media=False` und ohne
  Ausnahme instanziierte. Neuer optionaler `trusted_template_path` (API +
  CLI `--trusted-template` + ENV `ANONYMIZER_TRUSTED_TEMPLATE`) verifiziert
  `word/media`/`xl/media`-Einträge per SHA-256 gegen ein angegebenes
  Template; nur byte-identische Treffer passieren, jeder andere Medien-
  Eintrag sowie Embeddings/ActiveX/VBA/OLE bleiben unverändert gesperrt.
  Regressionstests: `test_trusted_template_media_hash_match_publishes`,
  `test_trusted_template_media_hash_mismatch_still_blocks`
  (`tests/test_security_boundaries.py`).
- [x] 2026-07-23: **Referenzlauf-Fund B — erst Symptom-Fix, dann strukturell
  behoben (RUN2-Nachbefund):** Der erste Fix (Wortlisten-Allowlist gegen
  "Landkreis Lörrach"/"Förderung"/"Zusage"/"Ablauf") war nur ein
  Symptom-Fix — deckte weder Flexionsformen ("Landkreises", Genitiv) noch
  das Grundproblem ab. Referenzlauf RUN2 bestätigte weiterhin
  sinnentstellende Fehl-Ersetzungen: "Grob bewegt Kim sich..." →
  "Amara Albrecht bewegt Lina sich...", "Beim Anziehen"/
  "Klettverschlüsse"/"Beim Essen"/"Reißverschlüssen"/
  "Einrichtungsangaben" → Fake-Namen, "Landkreises Lörrach" (Genitiv)
  weiter ersetzt. Strukturell nachgebessert: `_NER_KEEP_COMPONENTS`
  erweitert (tagger/morphologizer/lemmatizer/attribute_ruler zusätzlich zu
  tok2vec+ner) liefert `token.pos_`/`token.lemma_`; ein NER-PER-Span wird
  jetzt auf seine maximalen zusammenhängenden PROPN-Token-Teilsequenzen
  gekürzt (`_extract_name_token_runs`/`_is_name_token`) statt komplett
  verworfen/akzeptiert — mit Rettungsankern für Titel (Dr./Prof.) und
  bekannte Vornamen bei POS-Fehltagging (kein Pflichtanker: "Amara Diallo"
  ohne Lexikon-Eintrag bleibt über PROPN erkennbar). Gattungsbegriff-
  Denyliste zusätzlich auf LEMMA-Basis (`_tokens_pass_lemma_denylist`,
  deckt "Landkreises"→"Landkreis" ab); Oberflächenformen-Prüfung bleibt
  Fallback. Regressionstests mit den echten RUN2-Sätzen (skip-guarded auf
  installiertes `de_core_news_lg`); Kosten: mehr Pipeline-Komponenten pro
  Dokument (~3.600 Zeichen in ~0,25 s nach Warmup, keine praktisch
  relevante Verlangsamung in Tests). **ACHTUNG:** Dieser Fix erwies sich im
  Referenzlauf RUN3 als real SCHLECHTER als 0.2.1 (POS==PROPN allein zu
  durchlässig) — siehe direkt folgender Eintrag 0.2.3.
- [x] 2026-07-23: **RUN3-Regression zu 0.2.2 behoben — Anker-Prinzip
  (0.2.3, Operator-Design):** RUN3 mit der echten Akte zeigte reale
  Fehl-Ersetzungen von "Umgang", "Begleitung", "Handlauf", "Zähneputzen"
  sowie einen Abbruch von `prepare` über die Residualprüfung
  ("Beispiel"/"Umgang") — Ursache: spaCy misstaggt Substantive in
  Aufzählungs-/Fachtext-Kontexten häufig als PROPN, wodurch reines
  POS==PROPN als Kriterium durchlässiger statt strenger wurde.
  Ersetzungspolitik neu gestaffelt: `real_name`/`weitere_namen` immer
  ersetzt (unverändert); NER-PER-Mehrwort-Spans (≥2 Tokens) gelten als
  verifiziert; NER-PER-Einzelwort-Spans nur mit Anker (Lexikon-Vorname
  ODER vorangehendes Titel-/Anrede-Token Dr./Prof./Frau/Herr) — sonst
  landet der Treffer unzerstört im neuen Scan-Key `ner_review_only`
  (sichtbar, nicht im Ersetzungs-Mapping). `detect_person_names_ner()`
  gibt jetzt `(confirmed, review_only)` zurück. Residualprüfung
  entschärft sich dadurch von selbst (`_residual_originals()` prüfte
  schon vorher nur `profile.mappings`, jetzt gelangen dort einfach
  weniger Fehlalarme hinein). **Pflicht-DoD verifiziert:** volle
  pytest-Suite mit geladenem `de_core_news_lg` — 63 passed, 2 skipped
  (beide Windows-Symlink-OS-Limitationen, KEIN Modell-Test übersprungen),
  12 subtests; End-to-End-Realcheck `DocumentAnonymizer` gegen die echte
  RUN2-Akte (`ARCHIV_2026-07-23_RUN2/quelle/`) liefert unkorrumpierten
  Bericht — "Grob bewegt", "beim Umgang", "Klettverschlüsse",
  "Landkreises Lörrach", "Einrichtungsangaben", "die Förderung",
  "Begleitung", "Handlauf", "Zähneputzen" bleiben unverändert, "Kim" ist
  vollständig durch das Pseudonym ersetzt. Neue Tests:
  `test_run_has_anchor_single_word_needs_lexicon_or_title`,
  `test_ner_run2_regression_no_failure_class_tokens_confirmed_or_review`,
  `test_ner_run2_regression_positive_names_still_detected`,
  `test_ner_run2_real_akte_end_to_end_no_corruption` (skip-guarded, wenn
  der Referenzordner auf dem Host fehlt) (`tests/test_security_boundaries.py`).
- [x] 2026-07-16: Vollständiger Privacy-/Security-Review des 0.1.0-Snapshots;
  fail-closed Ordnerveröffentlichung, Pfad-/Symlink-/Cloud-Grenzen,
  transaktionale Einzeldatei-Verarbeitung, sichere Schlüsseldateien,
  vollständige Übernahme erkannter Namen/Institutionen und Domain-unabhängige
  E-Mail-Erkennung umgesetzt.
- [x] 2026-07-16: DOCX-/XLSX-OOXML-Flächen, PDF-Metadaten/Annotationen/Anhänge,
  Medienstopps, Ressourcenlimits, Restdatenprüfung und CLI-Vertrag mit
  Regressionstests abgesichert.
- [x] 2026-07-16: Unabhängigen Abschlussreview nachgearbeitet: NER-Modell- und
  Treffergrenzen, paketweite OOXML-Discovery inklusive Attribute/Charts,
  E-Mail-Casing, PDF-Bookmarks/Page-Labels, Windows-Reparse-Points und atomare
  Zielbaum-Veröffentlichung geschlossen; final 0×P0/P1/release-relevante P2.
- [x] 2026-07-16: README, WIRING, Manifest, Lizenz, Changelog, Security- und
  Release-Gate-Dokumentation auf den tatsächlichen Stand synchronisiert.
- [x] 2026-07-12: Wortgrenzen, Tabellenzeilen-Erkennung, Legacy-DOC,
  Absatz-Ersetzung und native Excel-Datumszellen aus dem BACH-Vorfall
  übernommen.
- [x] 2026-07-05: Build-Backend und Root-Übersicht gepflegt.
