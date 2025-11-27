import json
from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
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
    sql = text("DELETE FROM book_references WHERE citekey = :citekey")
    db.session.execute(
        sql,
        {
            "citekey": citekey,
        },
    )
    db.session.commit()

def update_reference(citekey, author, title, year, publisher):
    """Viitteen päivittäminen tietokantaan"""
    sql = text(
        "UPDATE book_references SET author = :author, title = :title, year = :year, publisher = :publisher WHERE citekey = :citekey"
    )
    db.session.execute(
        sql,
        {
            "citekey": citekey,
            "author": author,
            "title": title,
            "year": year,
            "publisher": publisher,
        },
    )
    db.session.commit()

def get_reference_by_key(citekey):
    """Hakee viitteen tietokannasta citekeyn perusteella"""
    sql = text(
        "SELECT citekey, author, title, year, publisher FROM book_references WHERE citekey = :citekey"
    )
    result = db.session.execute(
        sql,
        {
            "citekey": citekey,
        },
    )
    reference = result.fetchone()

    if reference is None:
        return None

    return Reference(
        reference[0], reference[1], reference[2], reference[3], reference[4]
    )
