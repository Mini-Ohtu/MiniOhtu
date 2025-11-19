CREATE TABLE book_references (
  id SERIAL PRIMARY KEY,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  publisher TEXT NOT NULL
);
