CREATE TABLE bibtex_references (
  id        SERIAL PRIMARY KEY,
  citekey   TEXT NOT NULL UNIQUE,
  entry_type TEXT NOT NULL,
  data      JSON NOT NULL
);

CREATE TABLE tags (
  id        SERIAL PRIMARY KEY,
  tag_name   TEXT NOT NULL UNIQUE
);

CREATE TABLE tag_references (
  id        SERIAL PRIMARY KEY,
  tag_id INTEGER REFERENCES tags ON DELETE CASCADE,
  reference_id INTEGER REFERENCES bibtex_references ON DELETE CASCADE
);
