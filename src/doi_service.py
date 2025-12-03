import re
from typing import Dict, Tuple

import requests

DOI_BASE_URL = "https://doi.org/"
ACCEPT_HEADER = "application/x-bibtex"


class DoiServiceError(Exception):
    """Raised when fetching or parsing DOI data fails."""


def _normalize_doi(doi: str) -> str:
    """Return DOI without protocol or host prefixes."""
    cleaned = (doi or "").strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    if not cleaned:
        raise DoiServiceError("DOI is required")
    return cleaned


def fetch_bibtex(doi: str) -> str:
    """Fetch a single BibTeX entry from the DOI service."""
    normalized = _normalize_doi(doi)
    url = f"{DOI_BASE_URL}{normalized}"
    response = requests.get(url, headers={"Accept": ACCEPT_HEADER}, timeout=10)
    if response.status_code >= 400:
        raise DoiServiceError(f"DOI lookup failed ({response.status_code})")
    content = response.text.strip()
    if not content:
        raise DoiServiceError("Empty response from DOI service")
    return content


def _coerce_value(value: str):
    """Strip wrapping quotes/braces and cast numeric strings to int."""
    cleaned = value.strip().strip(",")
    if (
        (cleaned.startswith("{") and cleaned.endswith("}"))
        or (cleaned.startswith('"') and cleaned.endswith('"'))
    ):
        cleaned = cleaned[1:-1]
    cleaned = cleaned.strip()
    if cleaned.isdigit():
        return int(cleaned)
    return cleaned


def _parse_header(bibtex: str) -> Tuple[str, str, str]:
    """Parse entry type and citekey; returns (entry_type, citekey, remainder)."""
    match = re.search(r"@\s*(\w+)\s*{\s*([^,]+)\s*,", bibtex, re.DOTALL)
    if not match:
        raise DoiServiceError("Could not parse BibTeX header")
    entry_type = match.group(1).strip().lower()
    citekey = match.group(2).strip()
    remainder = bibtex[match.end():]
    return entry_type, citekey, remainder


def _split_fields(body: str):
    """Split the fields section on top-level commas (ignoring commas inside braces/quotes)."""
    parts = []
    buf = []
    brace_depth = 0
    in_quote = False

    def flush():
        segment = "".join(buf).strip().rstrip(",")
        if segment:
            parts.append(segment)
        buf.clear()
        
    for ch in body:
        if ch == '"' and brace_depth == 0:
            in_quote = not in_quote
        elif not in_quote:
            if ch == "{":
                brace_depth += 1
            elif ch == "}" and brace_depth > 0:
                brace_depth -= 1
        if ch == "," and brace_depth == 0 and not in_quote:
            flush()
            continue

        buf.append(ch)
    flush()
    return parts


def _parse_fields(body: str) -> Dict[str, object]:
    """Parse BibTeX fields into a dictionary."""
    trimmed_body = body.strip()
    if trimmed_body.endswith("}"):
        trimmed_body = trimmed_body[:-1]

    fields: Dict[str, object] = {}
    for raw_field in _split_fields(trimmed_body):
        if "=" not in raw_field:
            continue
        key, raw_value = raw_field.split("=", 1)
        key = key.strip().lower()
        value = _coerce_value(raw_value)
        fields[key] = value
    if not fields:
        raise DoiServiceError("No fields parsed from BibTeX")
    return fields


def parse_bibtex_entry(bibtex: str) -> Dict[str, object]:
    """Convert a BibTeX entry string into the app's internal reference format."""
    if not bibtex or "@" not in bibtex:
        raise DoiServiceError("Invalid BibTeX payload")

    entry_type, citekey, remainder = _parse_header(bibtex)
    data = _parse_fields(remainder)

    return {
        "entry_type": entry_type,
        "citekey": citekey,
        "data": data,
    }


def fetch_reference_from_doi(doi: str) -> Dict[str, object]:
    """Fetch DOI as BibTeX and parse into a reference dict."""
    bibtex = fetch_bibtex(doi)
    return parse_bibtex_entry(bibtex)
