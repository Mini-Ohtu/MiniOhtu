from config import db, app
from sqlalchemy import text
import os

def _db_backend():
  return db.engine.url.get_backend_name()

def reset_db():
  print(f"Clearing contents from table book_references")
  sql = text(f"DELETE FROM book_references")
  db.session.execute(sql)
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
      sql = text(f"DROP TABLE {table}")
      db.session.execute(sql)
    db.session.commit()

  print("Creating database")
  
  schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
  with open(schema_path, 'r') as f:
    schema_sql = f.read().strip()

  if _db_backend() == "sqlite":
    schema_sql = schema_sql.replace(
      "SERIAL PRIMARY KEY",
      "INTEGER PRIMARY KEY AUTOINCREMENT"
    )
  
  sql = text(schema_sql)
  db.session.execute(sql)
  db.session.commit()

if __name__ == "__main__":
    with app.app_context():
      setup_db()
