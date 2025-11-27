CREATE TABLE bibtex_references (
  id        SERIAL PRIMARY KEY,
  citekey   TEXT NOT NULL UNIQUE,
  entry_type TEXT NOT NULL,
  data      JSON NOT NULL
);
