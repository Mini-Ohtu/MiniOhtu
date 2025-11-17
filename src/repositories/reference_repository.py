from config import db
from sqlalchemy import text

from entities.reference import Reference

def get_references():
    result = db.session.execute(text("SELECT author, title, year, publisher FROM references"))
    references = result.fetchall()
    return [Reference(reference[0], reference[1], reference[2], reference[3]) for reference in references] 

def create_references(content):
    sql = text("INSERT INTO references (content) VALUES (:content)")
    db.session.execute(sql, { "content": content })
    db.session.commit()