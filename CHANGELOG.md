# Changelog

## 2026-07-27 — Discoverability & Visual Architecture (Pfad B)

- **README Design & Badges:** Badges für Ecosystem (`ELLMOS / open-bricks`), LLM-Friendly (`llms.txt`), und Hygiene-Check (`2026-07-27`) eingebunden.
- **AI Agent Integration Callout:** GFM Note Callout (`> [!NOTE]`) für maschinelle Entdeckbarkeit und lokale KI-Agent-Anwendung vor externen LLM-Prompts ergänzt.
- **Mermaid Systemarchitektur:** Interaktives Mermaid-Ablaufdiagramm zur Visualisierung der Fail-Closed-Pipeline, spaCy-NER, Anker-Prüfung und Fernet-Schlüsselableitung hinzugefügt.
- **Maschinenlesbare Dokumentation (`llms.txt`):** `Last-checked` Zeitstempel auf 2026-07-27 aktualisiert.

## 2026-07-26 — Technische Hygiene & Maintenance

- **Testkonfiguration & Isolation (`pyproject.toml`):** `pythonpath = ["."]` in `[tool.pytest.ini_options]` hinterlegt für umgebungsunabhängiges Ausführen der Testsuite.
- **Maschinenlesbare Dokumentation (`llms.txt`):** `Last-checked` Zeitstempel auf 2026-07-26 aktualisiert mit verifizierten Testsuite-Ergebnissen (64 passed, 9 skipped).
- **Testsuite & CI Verification:** Vollständige Testsuite in isolierter Umgebung ausgeführt (64 passed, 9 skipped in 7.04s), 0 Fehler.

## 2026-07-24 — Discoverability & Doku

- **Maschinenlesbare Dokumentation (`llms.txt`):** Root-`llms.txt` angelegt für KI-Crawler, Agent-Discovery und strukturierte Übersicht der Fail-Closed-Sicherheitsverträge, Formate und CLI-/Python-APIs.
- **PyPI / GitHub Discovery Metadata:** Keywords (`anonymizer`, `pseudonymization`, `gdpr`, `dsgvo`, `ner`, `spacy`, `privacy-first`, `fail-closed`, `offline-first`) und `[project.urls]` in `pyproject.toml` hinterlegt.
- **README & Doku-Struktur:** Badges, Schnellübersichts-Tabellen und Suchbegriffe für maschinelles und menschliches Auffinden optimiert.

## 0.2.5 — 2026-07-23

- **Root Cause identifiziert (Referenzlauf RUN5, w6-Umgebungsvergleich):**
  Der 0.2.4-Fix wurde in einer anderen Umgebung (System-Python) reproduzierbar
  widerlegt — "Beim Anziehen"/"Beim Essen"/"Landkreises Lörrach" sowie neu
  "Kurze Notiz" wurden dort weiterhin ersetzt. Diagnose ergab: **keine**
  spaCy-/Modellversions-Drift (identische Versionen spacy==3.8.14,
  de_core_news_lg==3.8.0 in beiden Umgebungen, per `spacy.load(...).meta`
  verifiziert) — sondern ob zusätzlich **`en_core_web_lg` installiert ist**.
  War es das (System-Python, nicht in der eigenen venv), taggte das
  englische Modell deutschen Fließtext eigenständig fehlerhaft als
  `PERSON`/`PROPN` (z. B. "Beim"/"Anziehen"/"Notiz" alle PROPN, Lemma
  unverändert großgeschrieben) — die 0.2.2–0.2.4-Verteidigung (POS==PROPN +
  Lemma-Kleinschreibung) ist auf deutsche Lemmatisierungsregeln zugeschnitten
  und greift gegen dieses Muster nicht.
- **Modellversions-robuste Oberflächen-Härtung (Operator-Design):** Neue
  Regeln, die NICHT von POS/Lemma abhängen, laufen VOR der Mehrwort-/
  Anker-Entscheidung: (a) Präposition-Artikel-Kontraktionen ("Beim", "Zum",
  "Zur", "Am", "Im", "Ins", "Vom", "Übers", "Unterm") werden per
  Oberflächen-Exaktvergleich immer verworfen. (b) Gattungsbegriff-Denyliste
  zusätzlich per Oberflächen-Präfixmatch (Genitiv/Plural-Endungen, kein
  Lemma nötig). (c) Ein Token, das eine NEUE Teilsequenz eröffnen würde und
  dessen Kleinschreibform ein bekanntes deutsches Wort ist (`is_oov=False`,
  **immer gegen das DE-Vokabular geprüft**, unabhängig davon welches Modell
  den Tag erzeugt hat) und kein bekannter Vorname/Titel ist, gilt als
  generisches Wort ("Kurze Notiz") und wird verworfen — Tokens, die eine
  bereits akzeptierte Teilsequenz fortsetzen (Vorname+Nachname-Muster wie
  "Anna Muster"/"Anna Muster-Bergmann"), bleiben ausgenommen.
- **Sicherheitsnetz gegen Kollisionen:** `is_oov` unterscheidet nicht
  zuverlässig "generisches Wort" von "Name mit Vektor" — empirisch waren
  sowohl "kim" als auch "beispiel" im DE-Vokabular NICHT out-of-vocabulary.
  Mindestlänge 5 Zeichen für den Alltagswort-Check schützt kurze echte Namen
  ("Kim"); die "neue Teilsequenz"-Beschränkung schützt Nachnamen, die
  zufällig Alltagswörter sind ("Muster", "Bergmann"), solange sie einem
  bereits akzeptierten Vornamen folgen.
- **Denyliste erweitert:** "frühförderin"/"frühförderer"/"erzieher(in)"/
  "bezugserzieher(in)"/"sachbearbeiter(in)" ergänzt (eigener Fund beim
  End-to-End-Test: "Frühförderin Frau" wurde vom englischen Modell als
  2-Wort-PERSON-Span fehlgetaggt und über die Mehrwort-Regel bestätigt).
- **DoD in BEIDEN Umgebungen verifiziert:** eigene venv (nur `de_core_news_lg`)
  und System-Python (zusätzlich `en_core_web_lg`, reproduziert RUN5). Beide
  grün: venv 70 passed/3 skipped, System-Python 71 passed/2 skipped (jeweils
  nur die 2 Windows-Symlink-OS-Limitationen, kein Modell-Test übersprungen).
  End-to-End gegen die echte RUN2-Akte in BEIDEN Umgebungen: Profil-Mapping
  korrekt, "Beim Anziehen"/"Beim Essen"/"Landkreises Lörrach"/"Kurze Notiz"
  wörtlich unverändert im Output, Klientenname vollständig ersetzt.
- **README-Abschnitt "Modellversions-Sensitivität"** ergänzt: empfohlene/
  getestete Version (`de_core_news_lg==3.8.0`, `spacy==3.8.14`), Hinweis zum
  `en_core_web_lg`-Risiko, Versions-Pin als Kommentar in `pyproject.toml`.
- **CI-Nachbesserung (Testfehler, keine Verhaltensänderung):** GitHub Actions
  (kein spaCy-Modell installiert) schlug bei
  `test_harden_run_surface_drops_contraction_regardless_of_pos` fehl. Ursache
  war NICHT ein "Fail-open" der Kontraktions-/Denyliste-Schichten (a)/(b) —
  diese sind bereits rein oberflächenbasiert und vollständig modellfrei
  (kein `_get_spacy_model`-Zugriff) — sondern eine zu weit gefasste
  Testerwartung, die implizit voraussetzte, dass Schicht (c) (is_oov,
  modellabhängig, korrekt geguarded: ohne Modell → übersprungen) das zweite
  Token ebenfalls entfernt. Test korrigiert (zweites Token unter der
  Mindestlänge von Schicht (c), damit die Erwartung in JEDER Umgebung
  deterministisch ist) und in drei Kontexten verifiziert: eigene venv (70
  passed/3 skipped), System-Python mit `en_core_web_lg` (71 passed/2
  skipped), frische modellfreie venv als echte CI-Nachbildung (64 passed/9
  skipped, davon 7 korrekt übersprungene modellabhängige Tests).

## 0.2.4 — 2026-07-23

- **Mehrwort-Span-Härtung (Referenzlauf RUN4, Feinschliff zu 0.2.3):** Das
  Anker-Prinzip griff bereits korrekt für Einzelwort-Spans, aber
  Mehrwort-Spans umgingen es weiterhin: „Beim Anziehen"/„Beim Essen"
  (substantivierte Verben, teils fälschlich als PROPN getaggt) und
  „Landkreises Lörrach" (Genitiv, Gattungsbegriff + Eigenname im selben
  Span) wurden über die bisherige „≥2 Tokens = verifiziert"-Regel trotzdem
  ersetzt.
- **Trim VOR der Mehrwort-Akzeptanz (Operator-Design):** `_is_name_token()`
  prüft bei PROPN-getaggten Tokens jetzt zusätzlich das LEMMA als
  Gegenprobe: (a) Tokens, deren Lemma auf der Gattungsbegriff-Denyliste
  steht (Lemma von „Landkreises" ist „Landkreis"), werden aus dem Span
  gekürzt; (b) Tokens mit kleingeschriebenem Lemma — substantivierte
  Verben behalten ihr Infinitiv-Lemma, z. B. „Anziehen" → Lemma
  „anziehen" — werden ebenfalls gekürzt. Der gekürzte Rest durchläuft die
  normale Logik: ≥2 Tokens → weiterhin verifiziert, 1 Token → Anker-Regel
  (0.2.3), 0 Tokens → nichts. „Landkreises Lörrach" wird so zu „Lörrach"
  ohne Vornamen-/Titel-Anker → `ner_review_only` statt Ersetzung.
  Bindestrich-Doppelnamen („Anna Muster-Bergmann") bleiben unangetastet,
  da beide Teile echte PROPN-Nachnamen ohne Gattungsbegriff-/Verb-Lemma
  sind.
- **DoD verifiziert:** pytest mit geladenem `de_core_news_lg` — 65 passed,
  2 skipped (beide Windows-Symlink-OS-Limitationen, kein Modell-Test
  übersprungen), 14 subtests. End-to-End gegen die echte RUN2-Akte: das
  Profil-Namens-Mapping ist exakt {Kim, Beispiel, Kim Beispiel,
  Test-Fiktiv, Test-Mustermann, Sachbearbeiter-Fiktiv} — die tatsächlichen
  Personen im Text, keine Fehlklasse mehr darunter.

## 0.2.3 — 2026-07-23

- **Regression zu 0.2.2 (ehrlich dokumentiert):** Referenzlauf RUN3 mit der
  echten synthetischen Akte zeigte, dass 0.2.2 real SCHLECHTER war als
  0.2.1 — `prepare` brach über die Residualprüfung ab ("Beispiel"/"Umgang"),
  und zusätzlich wurden "Umgang", "Begleitung", "Handlauf", "Zähneputzen"
  fälschlich ersetzt; "Klettverschlüsse"/"Landkreises" blieben ebenfalls
  betroffen. Ursache: reines POS==PROPN als Akzeptanzkriterium kippt in der
  Praxis zu durchlässig — spaCy misstaggt Substantive in Aufzählungs-/
  Fachtext-Kontexten häufig als PROPN, wodurch der 0.2.2-Filter
  durchlässiger statt strenger wurde.
- **Anker-Prinzip als struktureller Nachfolger (Operator-Design):**
  Ersetzungspolitik neu gestaffelt: (i) `real_name`/`weitere_namen` werden
  weiterhin immer ersetzt (Kernzweck, unverändert). (ii) NER-PER-Mehrwort-
  Spans (≥2 Tokens nach der PROPN-Kürzung, Vor+Nachname-Muster) gelten als
  hinreichend verifiziert, deckt auch Namen ohne Lexikon-Eintrag wie "Amara
  Diallo" ab. (iii) NER-PER-Einzelwort-Spans werden NUR mit Anker ersetzt:
  bekannter Vorname (Lexikon) ODER unmittelbar vorangehendes Titel-/
  Anrede-Token (Dr./Prof./Frau/Herr). Ohne Anker: keine destruktive
  Ersetzung, stattdessen sichtbarer, nicht-destruktiver Review-Kandidat im
  neuen Scan-Ergebnis-Key `ner_review_only` (`create_profile()` liest
  diesen Key bewusst nicht). Die 0.2.2-Lemma-Denyliste bleibt als
  zusätzliche Schicht bestehen. `detect_person_names_ner()` gibt jetzt
  `(confirmed, review_only)` statt einer flachen Liste zurück.
- **Residualprüfung "entschärft sich von selbst":** `_residual_originals()`
  prüfte schon vorher ausschließlich `profile.mappings` (tatsächlich zu
  ersetzende Werte), nicht alle je gescannten Kandidaten — der RUN3-Abbruch
  kam davon, dass unter 0.2.2 zu viele generische Fehlalarme überhaupt erst
  ins Profil-Mapping gelangten. Mit dem Anker-Prinzip gelangen nur noch
  vertrauenswürdige Namen ins Mapping, wodurch die Residualprüfung ohne
  eigene Codeänderung wieder korrekt greift.
- **Pflicht-DoD verifiziert:** `DocumentAnonymizer` End-to-End (scan →
  create_profile → anonymize_folder) gegen die echte synthetische
  RUN2-Akte (`ARCHIV_2026-07-23_RUN2/quelle/`) liefert einen vollständig
  unkorrumpierten Bericht — "Grob bewegt", "beim Umgang", "Klettverschlüsse",
  "Landkreises Lörrach", "Einrichtungsangaben", "die Förderung", "Begleitung",
  "Handlauf", "Zähneputzen" bleiben unverändert erhalten; der Klientenname
  "Kim" ist vollständig und konsistent durch das Pseudonym ersetzt. Neuer
  Regressionstest `test_ner_run2_real_akte_end_to_end_no_corruption`
  (skip-guarded, wenn der Referenzordner auf dem Host fehlt).

## 0.2.2 — 2026-07-23

- **NER-Plausibilitätsfilter strukturell auf POS/Lemma umgestellt**
  (foerderplaner-Referenzlauf RUN2, Nachbefund zu 0.2.1): Die reine
  Wortlisten-Allowlist aus 0.2.1 war nur ein Symptom-Fix — sie deckte weder
  Flexionsformen ("Landkreises", Genitiv) noch das Grundproblem ab, dass
  Großschreibung im Deutschen KEIN Personen-Signal ist (jedes Substantiv
  wird großgeschrieben). Reale, weiterhin sinnentstellende Fehl-Ersetzungen
  aus RUN2: "Grob bewegt Kim sich..." → "Amara Albrecht bewegt Lina
  sich...", "Beim Anziehen"/"Klettverschlüsse"/"Beim Essen"/
  "Reißverschlüssen"/"Einrichtungsangaben" → Fake-Namen, "Landkreises
  Lörrach" (Genitiv) weiter ersetzt.
  - `_NER_KEEP_COMPONENTS` erweitert (tagger/morphologizer/lemmatizer/
    attribute_ruler zusätzlich zu tok2vec+ner; nur `parser` bleibt
    ausgeschlossen) — liefert `token.pos_`/`token.lemma_`.
  - Neue Span-Validierung: ein NER-PER-Span wird auf seine maximalen
    zusammenhängenden PROPN-Token-Teilsequenzen gekürzt
    (`_extract_name_token_runs`/`_is_name_token`) statt komplett verworfen
    oder komplett akzeptiert zu werden — mit begrenzten Rettungsankern für
    Titel-Token (Dr./Prof.) und bekannte deutsche Vornamen bei
    POS-Fehltagging (kein Pflichtanker: unbekannte Namen wie "Amara
    Diallo" bleiben allein über PROPN erkennbar).
  - Gattungsbegriff-Denyliste zusätzlich auf LEMMA-Basis geprüft
    (`_tokens_pass_lemma_denylist`) — deckt Flexionsformen ab
    ("Landkreises" → Lemma "Landkreis"); die bisherige
    Oberflächenformen-Prüfung bleibt als Fallback bestehen.
  - Regressionstests mit den echten RUN2-Sätzen (skip-guarded auf
    installiertes `de_core_news_lg`): nur "Kim" bleibt in den
    Fehlalarm-Sätzen übrig, "Landkreises Lörrach"/"Einrichtungsangaben"
    werden nicht mehr erfasst; "Kim Beispiel", "Dr. Anna Muster" und das
    lexikonfreie "Amara Diallo" bleiben erkannt.
  - Kosten: mehr Pipeline-Komponenten pro Dokumentdurchlauf (POS-Tagging/
    Lemmatisierung); in Tests keine praktisch relevante Verlangsamung
    (~3.600 Zeichen in ~0,25 s nach Modell-Warmup).

## 0.2.1 — 2026-07-23

- Git-Repository initialisiert (Branch `main`), GitHub-Actions-CI angelegt
  (Python 3.11/3.12-Matrix auf ubuntu-latest, Lint-Job, Bandit-Job).
- OOXML-Parsing gehärtet: `xml.etree.ElementTree` durch `defusedxml.ElementTree`
  ersetzt (3 Stellen in `core.py`, XML-Entity-/Billion-Laughs-Schutz beim
  Einlesen von DOCX-/XLSX-Daten); `defusedxml` als Pflichtabhängigkeit ergänzt.
  Bandit (`bandit -r anonymizer_modul -ll`) danach ohne Befunde.
- README um den Abschnitt „Rechtlicher Rahmen und Verantwortung" ergänzt:
  Pseudonymisierung ≠ Anonymisierung (DSGVO), § 203 StGB-Hinweis für
  Berufsgeheimnisträger, englische Kurzfassung.
- Realer NER-Qualitätstest mit `de_core_news_lg` gegen ausschließlich
  synthetische Namen durchgeführt (Ergebnis: `TODO.md`).
- Public-Metadaten vorbereitet: README-Kopfsatz, `pyproject.toml`-Beschreibung
  und `ellmos-module.json`-`visibility` (→ `public-candidate`) von der
  bisherigen "PRIVAT"-Kennzeichnung befreit; tatsächliche Veröffentlichung
  bleibt ein separater Freigabeschritt (/repo-publish-check, Operator).
- **Template-Medien-Fix (foerderplaner-Referenzlauf, Fund A):** DOCX/XLSX mit
  eingebetteten Bildern (z. B. Briefkopf-Logo im Berichts-Template) blockierten
  bisher IMMER die Ver-/De-Anonymisierung (`_has_unverified_package_content`
  ohne Ausnahme). Neuer optionaler `trusted_template_path` (API + CLI
  `--trusted-template` + ENV `ANONYMIZER_TRUSTED_TEMPLATE`) lässt gezielt
  `word/media`/`xl/media`-Einträge passieren, deren SHA-256-Hash
  byte-identisch aus dem angegebenen Template stammt; jeder andere Medien-
  Eintrag sowie Embeddings/ActiveX/VBA/OLE bleiben unverändert gesperrt
  (fail-closed-Prinzip erhalten). `DocumentDeanonymizer.deanonymize_file`/
  `deanonymize_folder` geben den Parameter durch, statt intern immer mit
  Default-`DocumentAnonymizer()` zu arbeiten.
- **NER-Plausibilitätsfilter erweitert (foerderplaner-Referenzlauf, Fund B):**
  `de_core_news_lg` markierte generische Verwaltungs-/Berichtssubstantive
  ("Landkreis Lörrach", "Förderung", "Zusage", "Ablauf") fälschlich als
  Personennamen. `_looks_like_person_name()` prüft Gattungsbegriffe jetzt an
  JEDER Wortposition (nicht mehr nur bei Einzelwort-Treffern) gegen eine
  erweiterte Verwaltungs-/Einrichtungs-/Berichtsvokabular-Liste
  (`_NER_GENERIC_REPORT_NOUNS`); die Stoppwortliste für satzfragment-
  verdächtige Spans wurde um Reflexivpronomen und Modal-/Hilfsverben ergänzt.
  Echte synthetische Namen ("Kim", "Anna Muster") bleiben erkannt.

## 0.2.0 — 2026-07-16

- Ordnerverarbeitung transaktional und fail-closed gemacht; nicht unterstützte
  Formate, Parserfehler, Symlinks und Pfadkollisionen veröffentlichen nichts.
- Schlüsselpfade gegen Traversal, Cloud-Sync und Symlinks geschützt;
  verschlüsselte Dateien atomar mit privaten Berechtigungen geschrieben und
  begrenzt gelesen.
- Alle gültigen E-Mail-Domains sowie erkannte Tabellen-/NER-Namen und
  Institutionen in die Profilbildung aufgenommen; fehlendes NER ist im
  Standardmodus ein harter Stop.
- DOCX-/XLSX-OOXML-Oberflächen erweitert und nach dem Speichern auf Restdaten
  geprüft; Discovery erfasst paketweit Texte und identitätstragende Attribute
  einschließlich Chart-/Drawing-Flächen; nicht verifizierte Medien werden
  standardmäßig abgelehnt.
- PDF-Metadaten, XML-Metadaten, Annotationen, Links, Formulare und Anhänge
  sowie Bookmarks und Page-Labels entfernt; bildhaltige PDFs ohne OCR abgelehnt;
  angeforderte Verschlüsselung fällt nicht mehr auf Klartext zurück.
- spaCy-Installationen ohne ladbares Modell und unplausibel große NER-Blöcke
  stoppen den Standard-Scan; E-Mail-Ersetzung ist casing-sicher.
- Windows-Junctions/Reparse-Points werden wie Symlinks abgelehnt; vollständige
  Zielbäume werden erst über eine gleichvolumige atomare Umbenennung publiziert.
- Legacy-DOC-Eingabe, Konvertierung und Ausgabe begrenzt.
- Reale CLI-Unterbefehle mit verdeckter Eingabe und belastbaren Exitcodes
  ergänzt.
- Dokumentation und tatsächliche foerderplaner-Verkabelung synchronisiert.

## 0.1.0 — 2026-06-27

- Standalone-Extraktion aus BACH v1.2.0 mit neutralisierten Laufzeitpfaden.
