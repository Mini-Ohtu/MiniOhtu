import re
from typing import Callable


def _clean_token(text: str) -> str:
    """Keep only ASCII letters/digits from text."""
    return re.sub(r"[^A-Za-z0-9]", "", text or "")


def _extract_last_name(author: str) -> str:
    """
    Extract last name from the first listed author.
    Supports "Last, First" and "First Last" forms; returns cleaned token.
    """
    if not author:
        return ""

    first_author = re.split(r"\s+and\s+", author, flags=re.IGNORECASE)[0].strip()
    if "," in first_author:
        last_name = first_author.split(",", 1)[0].strip()
    else:
        parts = first_author.split()
        last_name = parts[-1].strip() if parts else ""

    cleaned = _clean_token(last_name)
    if not cleaned:
        return ""
    return cleaned[0].upper() + cleaned[1:]


def _keyword_from_title(title: str) -> str:
    """Build keyword from first letters of each word in the title."""
    if not title:
        return ""
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "".join(word[0].lower() for word in words if word)


def _normalize_year(year) -> str:
    """Return numeric year part (4 digits max)."""
    if year is None:
        return ""
    digits = "".join(ch for ch in str(year) if ch.isdigit())
    return digits[:4]


def build_base_citekey(author: str, year, title: str) -> str:
    """Return base citekey: LastName + Year + keyword(initials)."""
    last_name = _extract_last_name(author)
    year_part = _normalize_year(year)
    keyword = _keyword_from_title(title)

    base = f"{last_name}{year_part}{keyword}"
    cleaned = _clean_token(base)
    return cleaned or "ref"


def generate_citekey(
    author: str, year, title: str, exists_fn: Callable[[str], bool]
) -> str:
    """
    Generate citekey and ensure uniqueness by appending incremental suffix.
    exists_fn should return True if citekey already exists.
    """
    base = build_base_citekey(author, year, title)
    candidate = base
    counter = 1
    while exists_fn(candidate):
        candidate = f"{base}{counter}"
        counter += 1
    return candidate
