import json
import re
from sqlalchemy import text
from werkzeug.datastructures import MultiDict
from config import db

from entities.reference import Reference


def get_references() -> list:
    """Viitteiden haku, huomioi if-vaihtoehto jos ei viitteitä löydy tietokannasta"""
    result = db.session.execute(
        text("SELECT citekey, entry_type, data FROM bibtex_references")
    )
    references = result.fetchall()

    if not references:
        return "Ei viitteitä"

    parsed_references = []
    for citekey, entry_type, data in references:
        payload = data
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                payload = {}
        if not isinstance(payload, dict):
            payload = {}

        parsed_references.append(
            Reference(
                citekey,
                entry_type,
                payload,
            )
        )

    return parsed_references


def get_filtered_references(args: MultiDict[str, str]) -> list:
    result_list = get_references()

    if len(args) == 0 or not isinstance(result_list, list):
        return result_list

    for key, value in args.items(multi=True):
        holder = []
        for result in result_list:
            search = ""
            if hasattr(result, key):
                search = str(getattr(result, key))
            else:
                search = str(result)
            string_result = re.findall(value, search, flags=re.IGNORECASE)
            if len(string_result) > 0:
                holder.append(result)

        result_list = holder

    if len(result_list) < 1:
        return "Ei viitteitä haussa/filterillä."

    return result_list


def make_citekey_unique(citekey: str) -> str:
    candidate = citekey
    suffix = 1
    while citekey_exists(candidate):
        candidate = f"{citekey}#{suffix}"
        suffix += 1
    return candidate


def create_references(citekey, entry_type, data):
    """Viitteiden luominen tietokantaan"""
    cleaned_data = {}
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, str):
            trimmed = value.strip()
            if trimmed == "":
                continue
            cleaned_data[key] = trimmed
        else:
            cleaned_data[key] = value
    citekey_to_store = make_citekey_unique(citekey)
    sql = text(
        "INSERT INTO bibtex_references (citekey, entry_type, data) VALUES (:citekey, :entry_type, :data)"
    )
    db.session.execute(
        sql,
        {
            "citekey": citekey_to_store,
            "entry_type": entry_type,
            "data": json.dumps(cleaned_data),
        },
    )
    db.session.commit()


def delete_reference(citekey):
    """Viitteiden poisto tietokannasta"""
    sql = text("DELETE FROM bibtex_references WHERE citekey = :citekey")
    db.session.execute(
        sql,
        {
            "citekey": citekey,
        },
    )
    db.session.commit()


def update_reference(citekey, data):
    """Viitteen päivittäminen tietokantaan"""
    existing = get_reference_by_key(citekey)
    merged = dict(existing.data) if existing else {}

    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, str):
            trimmed = value.strip()
            if trimmed == "":
                continue
            merged[key] = trimmed
        else:
            merged[key] = value

    sql = text("UPDATE bibtex_references SET data = :data WHERE citekey = :citekey")
    db.session.execute(
        sql,
        {
            "citekey": citekey,
            "data": json.dumps(merged),
        },
    )
    db.session.commit()


def get_reference_by_key(citekey):
    """Hakee viitteen tietokannasta citekeyn perusteella"""
    sql = text(
        "SELECT citekey, entry_type, data FROM bibtex_references WHERE citekey = :citekey"
    )
    result = db.session.execute(
        sql,
        {
            "citekey": citekey,
        },
    )
    row = result.fetchone()

    if row is None:
        return None

    citekey, entry_type, data = row
    payload = data
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {}
    if not isinstance(payload, dict):
        payload = {}

    return Reference(citekey, entry_type, payload)


def citekey_exists(citekey: str) -> bool:
    """Return True if citekey is already stored."""
    sql = text("SELECT 1 FROM bibtex_references WHERE citekey = :citekey LIMIT 1")
    result = db.session.execute(sql, {"citekey": citekey})
    return result.fetchone() is not None
