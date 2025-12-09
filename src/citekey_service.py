import random
import re
from typing import Callable


_STOP_WORDS = {
    "a",
    "an",
    "the",
    "in",
    "on",
    "at",
    "of",
    "for",
    "to",
    "by",
    "and",
    "or",
    "with",
    "from",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "vs",
}


def _clean_token(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", text or "")


def _extract_last_name(author: str) -> str:
    if not author:
        return ""
    normalized = re.sub(r"\s+", " ", author).strip()
    first_author = re.split(r"\band\b", normalized, maxsplit=1, flags=re.IGNORECASE)[0].strip()
    if "," in first_author:
        last_name = first_author.split(",", 1)[0].strip()
    else:
        parts = first_author.split()
        last_name = parts[-1].strip() if parts else ""

    cleaned = _clean_token(last_name)
    if not cleaned:
        return ""
    return cleaned[0].upper() + cleaned[1:]


def _significant_words(title: str) -> list[str]:
    if not title:
        return []
    words = re.findall(r"[A-Za-z0-9]+", title)
    significant = []
    for word in words:
        if word.lower() in _STOP_WORDS:
            continue
        cleaned = _clean_token(word)
        if not cleaned:
            continue
        significant.append(cleaned[0].upper() + cleaned[1:])
    return significant


def _random_significant_word(title: str) -> str:
    options = _significant_words(title)
    if not options:
        return ""
    # Pseudorandomness is fine for citekey variety (not security-sensitive).
    return random.choice(options)


def _normalize_year(year) -> str:
    if year is None:
        return ""
    digits = "".join(ch for ch in str(year) if ch.isdigit())
    return digits[:4]


def build_base_citekey(author: str, year, title: str) -> str:
    last_name = _extract_last_name(author)
    year_part = _normalize_year(year)
    keyword = _random_significant_word(title)

    base = f"{last_name}{year_part}{keyword}"
    cleaned = _clean_token(base)
    return cleaned or "ref"


def generate_citekey(
    author: str, year, title: str, exists_fn: Callable[[str], bool]
) -> str:
    base = build_base_citekey(author, year, title)
    candidate = base
    counter = 1
    while exists_fn(candidate):
        candidate = f"{base}{counter}"
        counter += 1
    return candidate
