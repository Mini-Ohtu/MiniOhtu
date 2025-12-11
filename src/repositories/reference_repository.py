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


def get_filtered_references(args: MultiDict[str, str], tag_id = None) -> list:
    if not tag_id:
        result_list = get_references()
    else:
        result_list = get_references_with_tag(tag_id)

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
        return "No references found with the given search/filter."

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
        "INSERT INTO bibtex_references (citekey, entry_type, data) "
        "VALUES (:citekey, :entry_type, :data)"
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

def create_tag(tag_name):
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
    return tag_id[0]

def add_tag_to_reference(tag_id, reference_id):
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
        text("SELECT id, tag_name FROM tags")
    )
    tags = result.fetchall()
    return tags

def get_tags_by_reference(reference_id):
    """Hakee kaikki viitteen tagit."""
    sql = text("""
        SELECT *
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

def get_tag_by_id(tag_id):
    """Hakee tagin id:n perusteella."""
    sql = text(
        "SELECT * FROM tags WHERE id = :id"
    )
    result = db.session.execute(
        sql,
        {
            "id": tag_id,
        },
    )
    row = result.fetchone()
    if row is None:
        return None
    return row

def get_tags_not_in_reference(reference_id):
    """Hakee tagit, joita ei ole lisätty kyseiseen viitteeseen."""
    sql = text("""
        SELECT t.*
        FROM tags t
        WHERE t.id NOT IN (
            SELECT tr.tag_id
            FROM tag_references tr
            WHERE tr.reference_id = :reference_id   
        )""")
    result = db.session.execute(
        sql,
        {
            "reference_id": reference_id
        },
    )
    references_by_tag= result.fetchall()
    return references_by_tag

def get_references_with_tag(tag_id) -> list:
    """Hakee kaikki viitteet, joihin on lisätty kyseinen tagi."""
    sql = text("""
        SELECT citekey, entry_type, data
        FROM bibtex_references br
        JOIN tag_references t ON br.id = t.reference_id
        WHERE t.tag_id = :tag_id;
        """)
    result = db.session.execute(
        sql,
        {
            "tag_id": tag_id
        },
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

def citekey_exists(citekey: str) -> bool:
    """Return True if citekey is already stored."""
    sql = text("SELECT 1 FROM bibtex_references WHERE citekey = :citekey LIMIT 1")
    result = db.session.execute(sql, {"citekey": citekey})
    return result.fetchone() is not None
