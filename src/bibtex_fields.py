BIBTEX_FIELDS = {
    "book": [
        ["author", "title", "year", "publisher"],
        ["volume", "number", "series", "address", "edition", "month", "note", "key", "url", "tag"],
    ],
    "article": [
        ["author", "title", "journal", "year"],
        ["volume", "number", "pages", "month", "doi", "note", "key", "tag"],
    ],
    "booklet": [
        ["title"],
        ["author", "howpublished", "address", "month", "year", "note", "key", "tag"],
    ],
    "conference": [
        ["author", "title", "booktitle", "year"],
        ["editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note", "key","tag"],
    ],
    "inbook": [
        ["author", "editor", "title", "chapter", "pages", "publisher", "year"],
        ["volume", "number", "series", "type", "address", "edition", "month", "note", "key", "tag"],
    ],
    "incollection": [
        ["author", "title", "booktitle", "publisher", "year"],
        ["editor", "volume", "number", "series", "type", "chapter", "pages", "address", "edition", "month", "note", "key", "tag"],
    ],
    "inproceedings": [
        ["author", "title", "booktitle", "year"],
        ["editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note", "key", "tag"],
    ],
    "manual": [
        ["title"],
        ["author", "organization", "address", "edition", "month", "year", "note", "key", "tag"],
    ],
    "mastersthesis": [
        ["author", "title", "school", "year"],
        ["type", "address", "month", "note", "key", "tag"],
    ],
    "misc": [
        [],
        ["author", "title", "howpublished", "month", "year", "note", "key", "tag"],
    ],
    "phdthesis": [
        ["author", "title", "school", "year"],
        ["type", "address", "month", "note", "key", "tag"],
    ],
    "proceedings": [
        ["title", "year"],
        ["editor", "volume", "number", "series", "address", "month", "publisher", "organization", "note", "key", "tag"],
    ],
    "techreport": [
        ["author", "title", "institution", "year"],
        ["type", "number", "address", "month", "note", "key", "tag"],
    ],
    "unpublished": [
        ["author", "title", "note"],
        ["month", "year", "key", "tag"],
    ],
}
