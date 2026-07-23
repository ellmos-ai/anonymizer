"""
anonymizer_modul — Standalone-Anonymizer für personenbezogene Dokumente
=======================================================================

PRIVAT — klientenbezogene Daten, nicht veröffentlichen.

Nutzung:
    from anonymizer_modul import DocumentAnonymizer, DocumentDeanonymizer, AnonymProfile

Minimales Beispiel (ohne pip-Extras):
    anon = DocumentAnonymizer()
    profile = anon.create_profile(
        real_name="Max Mustermann",
        geburtsdatum="15.03.2016",
    )
    success, count = anon.anonymize_file("bericht.txt", profile)

Verschlüsselung (pip install cryptography):
    from anonymizer_modul import encrypt_key_file, decrypt_key_file, get_key_path
    encrypt_key_file(profile, str(get_key_path(profile.client_id)), "meinPasswort")
    profile2 = decrypt_key_file(str(get_key_path(profile.client_id)), "meinPasswort")
"""

from .core import (
    # Haupt-Klassen
    DocumentAnonymizer,
    DocumentDeanonymizer,

    # Datenklassen
    AnonymProfile,
    AnonymResult,
    ProgressInfo,

    # Schlüssel-Funktionen
    encrypt_key_file,
    decrypt_key_file,
    get_local_keys_dir,
    get_key_path,

    # Generator-Helfer
    _generate_tarnname,
    _detect_gender,
    _shift_date,
    _generate_fake_phone,
    _generate_fake_email,
    _generate_fake_address,
    _generate_fake_institution,

    # Regex-Patterns (für direkte Nutzung)
    PHONE_PATTERN,
    EMAIL_PATTERN,
    STREET_PATTERN,
    INSTITUTION_PATTERN,

    # Verfügbarkeits-Flags
    CRYPTO_AVAILABLE,
    DOCX_AVAILABLE,
    FITZ_AVAILABLE,
    PIKEPDF_AVAILABLE,
    EXCEL_AVAILABLE,
)

__version__ = "0.2.4"
__all__ = [
    # Klassen
    "DocumentAnonymizer",
    "DocumentDeanonymizer",
    "AnonymProfile",
    "AnonymResult",
    "ProgressInfo",
    # Schlüssel
    "encrypt_key_file",
    "decrypt_key_file",
    "get_local_keys_dir",
    "get_key_path",
    # Generator-Helfer
    "_generate_tarnname",
    "_detect_gender",
    "_shift_date",
    "_generate_fake_phone",
    "_generate_fake_email",
    "_generate_fake_address",
    "_generate_fake_institution",
    # Patterns
    "PHONE_PATTERN",
    "EMAIL_PATTERN",
    "STREET_PATTERN",
    "INSTITUTION_PATTERN",
    # Flags
    "CRYPTO_AVAILABLE",
    "DOCX_AVAILABLE",
    "FITZ_AVAILABLE",
    "PIKEPDF_AVAILABLE",
    "EXCEL_AVAILABLE",
]
