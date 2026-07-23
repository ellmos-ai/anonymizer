# Changelog

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
