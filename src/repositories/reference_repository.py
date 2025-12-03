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
        return "No references"

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
            string_result = re.findall(value, search)
            if len(string_result) > 0:
                holder.append(result)

        result_list = holder

    if len(result_list) < 1:
        return "Ei viitteitä haussa/filterillä."

    return result_list


# pylint: disable=C0301
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
    sql = text(
        "INSERT INTO bibtex_references (citekey, entry_type, data) VALUES (:citekey, :entry_type, :data)"
    )
    db.session.execute(
        sql,
        {
            "citekey": citekey,
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

#tägien lisäys

def add_tag(tag_name):
    """Hakee tagin id:n tag_namen perusteella tai luo uuden tagin ja palauttaa sen id:n"""
    sql = text("SELECT id FROM tags WHERE tag_name = :tag_name")
    result = db.session.execute(
        sql,
        {
            "tag_name": tag_name,
        },
    )
    tag_id = result.fetchone()
    if tag_id:
        return tag_id[0]

    sql = text("""
        INSERT INTO tags (tag_name) 
        VALUES (:tag_name) 
        ON CONFLICT (tag_name) DO NOTHING
        RETURNING id
    """)
    result = db.session.execute(
        sql,
        {
            "tag_name": tag_name,
        },
    )
    db.session.commit()
    tag_id = result.fetchone()
    if tag_id:
        return tag_id[0]

def link_tag_to_reference(tag_id, reference_id):
    """Lisää tagin viitteeseen, jollei sitä ole jo lisätty."""
    sql = text("SELECT 1 FROM tag_references WHERE tag_id = :tag_id AND reference_id = :reference_id")
    result = db.session.execute(
        sql,
        {
            "tag_id": tag_id,
            "reference_id": reference_id,
        },
    )
    row = result.fetchone()
    if row:
        return False

    sql = text("""
        INSERT INTO tag_references (tag_id, reference_id) 
        VALUES (:tag_id, :reference_id) 
        ON CONFLICT DO NOTHING
    """)
    db.session.execute(
        sql,
        {
            "tag_id": tag_id,
            "reference_id": reference_id,
        },
    )
    db.session.commit()
    return True

def get_all_tags():
    """Hakee kaikki tagit."""
    result = db.session.execute(
        text("SELECT tag_name FROM tags")
    )
    tags = result.fetchall()
    return tags

def get_tags_by_reference(reference_id):
    """Hakee kaikki viitteen tagit."""
    sql = text("""
        SELECT tag_name
        FROM tags
        JOIN tag_references ON tags.id = tag_references.tag_id
        WHERE tag_references.reference_id = :reference_id;
        """)
    result = db.session.execute(
        sql,
        {
            "reference_id": reference_id
        },
    )
    tags_by_reference = result.fetchall()
    return tags_by_reference

def get_reference_id(citekey):
    """Hakee viitteen id:n citekeyn perusteella."""
    sql=text("SELECT id FROM bibtex_references WHERE citekey = :citekey")
    result = db.session.execute(
        sql,
        {
            "citekey": citekey
        },
    )
    reference_id = result.fetchone()[0]
    return reference_id
