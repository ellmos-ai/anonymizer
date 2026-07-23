#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
test_module_smoke.py — Round-Trip-Smoke-Test für das anonymizer-Modul
======================================================================

WICHTIG:
- Keine echten Klarnamen — nur fiktive (Max Mustermann, Frau Schmidt etc.)
- Kein BACH-Import
- Schlüssel nur in temporäres Verzeichnis (kein ~/.anonymizer oder OneDrive)
- Kern-Test läuft ohne pip-Extras (nur stdlib + anonymizer_modul)
- AES-Test wird übersprungen wenn cryptography nicht installiert

Ausführen:
    PYTHONIOENCODING=utf-8 python -m pytest tests/test_module_smoke.py -v
    # oder direkt:
    PYTHONIOENCODING=utf-8 python tests/test_module_smoke.py
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Modul-Pfad eintragen (kein BACH)
_HERE = Path(__file__).parent.parent
sys.path.insert(0, str(_HERE))

from anonymizer_modul.core import (  # noqa: E402
    DocumentAnonymizer,
    DocumentDeanonymizer,
    AnonymProfile,
    encrypt_key_file,
    decrypt_key_file,
    get_local_keys_dir,
    _generate_tarnname,
    _detect_gender,
    CRYPTO_AVAILABLE,
)


class TestImport(unittest.TestCase):
    """Prüft, dass das Modul ohne BACH importierbar ist."""

    def test_import_ohne_bach(self):
        """Modul-Import darf keinen bach_paths-Import auslösen."""
        # sys.modules darf kein bach_paths enthalten
        for key in sys.modules:
            self.assertNotIn("bach_paths", key, f"BACH-Modul in sys.modules: {key}")
            self.assertNotIn("bach.hub", key)

    def test_klassen_verfuegbar(self):
        """Haupt-Klassen müssen importierbar sein."""
        self.assertTrue(callable(DocumentAnonymizer))
        self.assertTrue(callable(DocumentDeanonymizer))


class TestGenderErkennung(unittest.TestCase):
    """Prüft die Gender-Erkennungsfunktion."""

    def test_maennliche_namen(self):
        """Männliche Namen werden als 'm' erkannt."""
        maennlich = ["Max", "Paul", "Leon", "Felix", "Jonas", "Thomas"]
        for name in maennlich:
            gender = _detect_gender(name)
            self.assertIn(gender, ('m', 'u'),
                          f"'{name}' sollte 'm' oder 'u' sein, ist aber '{gender}'")

    def test_weibliche_namen(self):
        """Weibliche Namen werden als 'w' erkannt."""
        weiblich = ["Marie", "Sophie", "Emma", "Lena", "Julia"]
        for name in weiblich:
            gender = _detect_gender(name)
            self.assertIn(gender, ('w', 'u'),
                          f"'{name}' sollte 'w' oder 'u' sein, ist aber '{gender}'")

    def test_unbekannte_namen(self):
        """Unbekannte Namen liefern 'm', 'w' oder 'u' — nie einen Fehler."""
        result = _detect_gender("Xyzqw")
        self.assertIn(result, ('m', 'w', 'u'))


class TestTarnnameGenerator(unittest.TestCase):
    """Prüft den Tarnnamen-Generator."""

    def test_tarnname_format(self):
        """Tarnname hat Format 'Vorname Nachname'."""
        name = _generate_tarnname()
        parts = name.split(" ")
        self.assertEqual(len(parts), 2, f"Kein 'Vorname Nachname'-Format: '{name}'")

    def test_tarnname_unterschiedlich(self):
        """Mehrere Aufrufe liefern (fast immer) verschiedene Namen."""
        namen = {_generate_tarnname() for _ in range(10)}
        self.assertGreater(len(namen), 1, "Alle 10 Tarnnamen sind identisch (unwahrscheinlich)")

    def test_keine_klarnamen(self):
        """Generierter Tarnname enthält keine bekannten Echtpersonen."""
        verbotene = ["Max Mustermann", "Frau Schmidt", "Dr. Meyer"]
        for _ in range(20):
            name = _generate_tarnname()
            for verboten in verbotene:
                self.assertNotIn(verboten, name)

    def test_kollisionsvermeidung(self):
        """Bereits verwendete Namen werden nicht nochmal generiert."""
        used = {"Felix Bergmann", "Emma Fischer", "Paul Lindner"}
        for _ in range(50):
            name = _generate_tarnname(used_names=used)
            self.assertNotIn(name, used)


class TestProfileErstellung(unittest.TestCase):
    """Prüft die Profil-Erstellung."""

    def setUp(self):
        self.anon = DocumentAnonymizer()

    def test_profil_hat_tarnname(self):
        """Profil enthält einen Tarnname."""
        profile = self.anon.create_profile(
            real_name="Max Mustermann",
            geburtsdatum="15.03.2016",
        )
        self.assertIsInstance(profile, AnonymProfile)
        self.assertTrue(profile.tarnname)
        self.assertNotEqual(profile.tarnname, "Max Mustermann")

    def test_profil_kein_klarname(self):
        """Tarnname darf nicht dem echten Namen entsprechen."""
        profile = self.anon.create_profile(
            real_name="Frau Schmidt",
            geburtsdatum="01.01.2010",
        )
        self.assertNotIn("Schmidt", profile.tarnname)

    def test_mappings_enthalten_hauptname(self):
        """Haupt-Mapping enthält den echten Namen."""
        profile = self.anon.create_profile(
            real_name="Max Mustermann",
            geburtsdatum="15.03.2016",
        )
        names_mapping = profile.mappings.get("names", {})
        self.assertIn("Max Mustermann", names_mapping,
                      f"'Max Mustermann' fehlt in mappings['names']: {names_mapping}")

    def test_geburtsdatum_verschoben(self):
        """Falsches Geburtsdatum ist verschieden vom echten."""
        profile = self.anon.create_profile(
            real_name="Max Mustermann",
            geburtsdatum="15.03.2016",
        )
        self.assertNotEqual(profile.fake_geburtsdatum, "15.03.2016")

    def test_client_id_eindeutig(self):
        """Jedes Profil bekommt eine eindeutige Client-ID."""
        ids = {
            self.anon.create_profile("Person A", "01.01.2010").client_id
            for _ in range(5)
        }
        self.assertGreater(len(ids), 1, "Alle Client-IDs sind identisch (unwahrscheinlich)")


class TestTextRoundTrip(unittest.TestCase):
    """
    Kern-Test: Text anonymisieren → de-anonymisieren → Original zurück.
    Läuft ohne pip-Extras (nur stdlib).
    """

    def setUp(self):
        self.anon = DocumentAnonymizer()
        self.profile = self.anon.create_profile(
            real_name="Max Mustermann",
            geburtsdatum="15.03.2016",
        )

    def test_anonymisierung_ersetzt_klarname(self):
        """Nach Anonymisierung ist der Klarname nicht mehr im Text."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("Für Max Mustermann wurde ein Förderplan erstellt.")
            tmp_path = Path(f.name)

        try:
            success, count = self.anon.anonymize_file(str(tmp_path), self.profile)
            self.assertTrue(success, "anonymize_file schlug fehl")
            self.assertGreater(count, 0, "Keine Ersetzungen durchgeführt")

            anon_text = tmp_path.read_text(encoding="utf-8")
            self.assertNotIn("Max Mustermann", anon_text,
                             f"Klarname noch im anonymisierten Text: {anon_text}")
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_round_trip_stellt_original_wieder_her(self):
        """
        Round-Trip: anonymisieren → de-anonymisieren → Original zurück.
        Schlüsselinformation kommt direkt aus dem Profil (kein Datei-Encrypt nötig).
        """
        original = "Für Max Mustermann wurde am 15.03.2016 ein Förderplan erstellt."

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(original)
            tmp_path = Path(f.name)

        try:
            # Schritt 1: Anonymisieren
            success1, count1 = self.anon.anonymize_file(str(tmp_path), self.profile)
            self.assertTrue(success1)
            self.assertGreater(count1, 0)

            anon_text = tmp_path.read_text(encoding="utf-8")
            self.assertNotIn("Max Mustermann", anon_text)

            # Schritt 2: De-anonymisieren
            deanon = DocumentDeanonymizer()
            success2, count2 = deanon.deanonymize_file(str(tmp_path), self.profile)
            self.assertTrue(success2, "deanonymize_file schlug fehl")

            restored = tmp_path.read_text(encoding="utf-8")
            self.assertIn("Max Mustermann", restored,
                          f"Klarname fehlt nach De-Anonymisierung: {restored}")
            self.assertEqual(restored, original,
                             f"Original nicht wiederhergestellt.\nErwartet: {original}\nGot: {restored}")
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_mehrere_namen_im_text(self):
        """Alle registrierten Namen werden ersetzt."""
        profile = self.anon.create_profile(
            real_name="Max Mustermann",
            geburtsdatum="15.03.2016",
            weitere_namen=["Frau Schmidt"],
        )
        original = "Max Mustermann wurde von Frau Schmidt betreut."

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(original)
            tmp_path = Path(f.name)

        try:
            success, count = self.anon.anonymize_file(str(tmp_path), profile)
            self.assertTrue(success)

            anon_text = tmp_path.read_text(encoding="utf-8")
            self.assertNotIn("Max Mustermann", anon_text)
            self.assertNotIn("Schmidt", anon_text)
        finally:
            tmp_path.unlink(missing_ok=True)


class TestAESSchluessel(unittest.TestCase):
    """
    Prüft AES-256-Schlüsselverschlüsselung.
    Wird übersprungen wenn cryptography nicht installiert.
    """

    @unittest.skipUnless(CRYPTO_AVAILABLE, "pip install cryptography erforderlich")
    def test_schluessel_round_trip(self):
        """Profil authentifiziert verschlüsseln → entschlüsseln → identisch."""
        anon = DocumentAnonymizer()
        profile = anon.create_profile(
            real_name="Max Mustermann",
            geburtsdatum="15.03.2016",
        )

        with tempfile.TemporaryDirectory() as tmpdir, mock.patch.dict(
            os.environ, {"ANONYMIZER_KEYS_DIR": tmpdir}
        ):

            schluessel_path = Path(tmpdir) / f"{profile.client_id}.schluessel.enc"
            passwort = "TestPasswort_2026!"

            # Verschlüsseln
            encrypt_key_file(profile, str(schluessel_path), passwort)
            self.assertTrue(schluessel_path.exists(),
                            "Schlüsseldatei wurde nicht erstellt")
            self.assertGreater(schluessel_path.stat().st_size, 16,
                               "Schlüsseldatei zu klein (nur Salt?)")

            # Entschlüsseln
            loaded = decrypt_key_file(str(schluessel_path), passwort)

            # Vergleichen
            self.assertEqual(loaded.client_id, profile.client_id)
            self.assertEqual(loaded.tarnname, profile.tarnname)
            self.assertEqual(loaded.fake_geburtsdatum, profile.fake_geburtsdatum)
            self.assertEqual(loaded.mappings, profile.mappings)

            # Falsches Passwort muss Fehler werfen
            with self.assertRaises(Exception):
                decrypt_key_file(str(schluessel_path), "FalschesPasswort!")

    @unittest.skipUnless(CRYPTO_AVAILABLE, "pip install cryptography erforderlich")
    def test_schluessel_nicht_in_onedrive(self):
        """get_local_keys_dir() zeigt nicht in einen OneDrive-Pfad (ohne ENV-Override)."""
        # ENV-Override löschen für diesen Test
        original = os.environ.pop("ANONYMIZER_KEYS_DIR", None)
        try:
            keys_dir = get_local_keys_dir()
            self.assertNotIn("OneDrive", str(keys_dir),
                             f"Schlüsselverzeichnis liegt in OneDrive: {keys_dir}")
        finally:
            if original:
                os.environ["ANONYMIZER_KEYS_DIR"] = original


class TestSensitiveDatenScan(unittest.TestCase):
    """Prüft das automatische Erkennen sensibler Daten im Text."""

    def setUp(self):
        # Diese Regex-Smokes prüfen bewusst nur die reduzierte Erkennung. Der
        # Produktionsstandard bleibt require_ner=True und schlaegt ohne NER
        # kontrolliert fehl.
        self.anon = DocumentAnonymizer(require_ner=False)

    def test_telefon_erkennung(self):
        """Telefonnummern werden erkannt."""
        text = "Rufen Sie uns unter 07761/123456 oder 0761 12345678 an."
        found = self.anon.scan_text_for_sensitive_data(text)
        self.assertGreater(len(found.get("phones", [])), 0,
                           f"Keine Telefonnummern gefunden in: {text}")

    def test_email_erkennung_alle_domains(self):
        """Alle syntaktisch gültigen E-Mail-Adressen sind sensibel."""
        text = "Kontakt: max.mustermann@gmail.com oder info@example.com"
        found = self.anon.scan_text_for_sensitive_data(text)
        emails = found.get("emails", [])
        self.assertIn("max.mustermann@gmail.com", emails)
        self.assertIn("info@example.com", emails)


class TestModulKonstanten(unittest.TestCase):
    """Prüft, dass keine BACH-Bezüge in den Strings sind."""

    def test_keine_bach_pfade_in_get_local_keys_dir(self):
        """get_local_keys_dir() darf keinen BACH-Pfad zurückgeben (ohne ENV-Override)."""
        import anonymizer_modul.core as core_mod

        # Den Quellcode auf 'BACH' und 'bach_paths' prüfen
        import inspect
        source = inspect.getsource(core_mod.get_local_keys_dir)
        self.assertNotIn("bach_paths", source)
        self.assertNotIn("BACH\\keys", source)
        self.assertNotIn("BACH/keys", source)

    def test_no_bach_import_in_modul(self):
        """Das Modul darf keinen 'bach_paths'-Import enthalten."""
        import inspect
        import anonymizer_modul.core as core_mod
        source = inspect.getsource(core_mod)
        self.assertNotIn("from bach_paths", source)
        self.assertNotIn("import bach_paths", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
