from __future__ import annotations


def is_non_empty_text(text: str | None) -> bool:
    return bool((text or "").strip())


def validate_contact(contact: str | None) -> bool:
    value = (contact or "").strip()
    if len(value) >= 3:
        return True
    return False
