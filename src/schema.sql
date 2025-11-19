CREATE TABLE book_references (
  id SERIAL PRIMARY KEY,
  citekey TEXT NOT NULL,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  publisher TEXT NOT NULL
);
