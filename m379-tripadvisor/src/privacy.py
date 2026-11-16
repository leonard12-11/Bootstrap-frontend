"""Pseudonymisierung, bevor Texte unseren Computer verlassen."""
import re

_TITLE = re.compile(r"\b(Mr|Mrs|Ms|Miss|Dr|Mister)\.?\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)?")
_NAMED = re.compile(r"\b(named|called|name is|name was)\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)?")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


def mask(text: str) -> str:
    """Ersetzt Namen nach Anrede/"named", E-Mails und Telefonnummern durch Platzhalter.

    Grenze: Vornamen ohne Anrede ("Maria at the front desk") werden NICHT erkannt.
    Darum zeigen wir im Report keine Zitate ohne Kontrolle von Hand.
    """
    text = _EMAIL.sub("[EMAIL]", text)
    text = _PHONE.sub("[TEL]", text)
    text = _TITLE.sub(lambda m: m.group(1) + " [NAME]", text)
    text = _NAMED.sub(lambda m: m.group(1) + " [NAME]", text)
    return text
