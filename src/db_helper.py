import os
from sqlalchemy import text
import sqlalchemy
from config import db, app


def _db_backend():
    return db.engine.url.get_backend_name()


def reset_db():
    print("Clearing contents from table bibtex_references")
    sql_references = text("DELETE FROM bibtex_references")
    db.session.execute(sql_references)

    print("Clearing contents from table tags")
    sql_tags = text("DELETE FROM tags")
    db.session.execute(sql_tags)

    print("Clearing contents from table tag_reference")
    sql_tag_reference = text("DELETE FROM tag_reference")
    db.session.execute(sql_tag_reference)

    db.session.commit()


def tables():
    """Returns all table names from the database except internal ones"""
    backend = _db_backend()
    if backend == "sqlite":
        sql = text(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    else:
        sql = text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public' "
            "AND table_name NOT LIKE '%_id_seq'"
        )
    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def setup_db():
    """
    Creating the database
    If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            drop_table = (
                f"DROP TABLE {table}" + " CASCADE" if _db_backend() != "sqlite" else ""
            )
            sql = text(drop_table)
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    # pylint: disable=W1514
    with open(schema_path, "r") as f:
        schema_sql = f.read().strip()

    if _db_backend() == "sqlite":
        schema_sql = schema_sql.replace(
            "SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT"
        ).replace("JSON NOT NULL", "TEXT NOT NULL")

    statements = schema_sql.split(";")
    for state in statements:

        state = state.strip()
        if len(state) == 0:
            continue

        sql2 = text(state)
        try:
            db.session.execute(sql2)
            db.session.commit()
        except sqlalchemy.exc.OperationalError as e:
            print(f"Here is the error: \n{e}")
            print("-----------")
        except sqlalchemy.exc.ProgrammingError as e2:
            print("You have tried to do something weird:")
            print(e2)


if __name__ == "__main__":
    with app.app_context():
        setup_db()
