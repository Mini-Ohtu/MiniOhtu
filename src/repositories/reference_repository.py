from config import db
from sqlalchemy import text

from entities.reference import Reference

def get_references():
    """ Viitteiden haku, huomioi if-vaihtoehto jos ei viitteitä löydy tietokannasta """
    result = db.session.execute(text("SELECT author, title, year, publisher FROM references"))
    references = result.fetchall()

    if not references:
        return "Ei viitteitä"
    
    return [Reference(reference[0], reference[1], reference[2], reference[3]) for reference in references] 

def create_references(author, title, year, publisher):
    """Viitteiden luominen tietokantaan"""
    sql = text("INSERT INTO references (author, title, year, publisher) VALUES (:author, :title, :year, :publisher)")
    db.session.execute(sql, {
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher})
    db.session.commit()
