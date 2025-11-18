CREATE TABLE todos (
  id SERIAL PRIMARY KEY, 
  content TEXT NOT NULL,
  done BOOLEAN DEFAULT FALSE
)

CREATE TABLE references (
  id SERIAL PRIMARY KEY,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INTEGER,
  publisher TEXT
)
