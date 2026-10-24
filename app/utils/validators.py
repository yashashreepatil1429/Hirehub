import re
from datetime import datetime
from typing import Any, Iterable

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+]?[(]?[0-9]{1,4}[)]?[-\s0-9]{6,15}$")


def is_valid_email(value: str) -> bool:
    return bool(value and EMAIL_RE.match(value.strip()))


def is_valid_phone(value: str) -> bool:
    return bool(value and PHONE_RE.match(value.strip()))


def is_valid_password(value: str) -> bool:
    return bool(value and len(value) >= 6)


def is_valid_object_id(value: Any) -> bool:
    return bool(value) and str(value).strip()


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    if isinstance(value, Iterable):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def validate_date(value: str) -> bool:
    if not value:
        return False
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def secure_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", (name or '').strip())
    return cleaned or 'resume'


def normalize_role(role: str | None) -> str:
    return (role or 'CANDIDATE').upper()
