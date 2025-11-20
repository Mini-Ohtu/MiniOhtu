from sqlalchemy import text
from config import db

from entities.reference import Reference


def get_references():
    """Viitteiden haku, huomioi if-vaihtoehto jos ei viitteitä löydy tietokannasta"""
    result = db.session.execute(
        text("SELECT citekey, author, title, year, publisher FROM book_references")
    )
    references = result.fetchall()

    if not references:
        return "Ei viitteitä"

    return [
        Reference(reference[0], reference[1], reference[2], reference[3], reference[4])
        for reference in references
    ]


# pylint: disable=C0301
def create_references(citekey, author, title, year, publisher):
    """Viitteiden luominen tietokantaan"""
    sql = text(
        "INSERT INTO book_references (citekey, author, title, year, publisher) VALUES (:citekey, :author, :title, :year, :publisher)"
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
