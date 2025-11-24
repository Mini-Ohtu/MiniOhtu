BIBTEX_FIELDS = {
    "book": {
        "required": [
            {"name": "author", "label": "Author *", "required": True},
            {"name": "title", "label": "Title *", "required": True},
            {"name": "year", "label": "Year *", "required": True},
            {"name": "publisher", "label": "Publisher *", "required": True},
        ],
        "optional": [
            {"name": "volume", "label": "Volume"},
            {"name": "number", "label": "Number"},
            {"name": "series", "label": "Series"},
            {"name": "address", "label": "Address"},
            {"name": "edition", "label": "Edition"},
            {"name": "month", "label": "Month"},
            {"name": "note", "label": "Note"},
            {"name": "key", "label": "Key"},
            {"name": "url", "label": "URL"},
        ],
    },
    "article": {
        "required": [
            {"name": "author", "label": "Author *", "required": True},
            {"name": "title", "label": "Title *", "required": True},
            {"name": "journal", "label": "Journal *", "required": True},
            {"name": "year", "label": "Year *", "required": True},
        ],
        "optional": [
            {"name": "volume", "label": "Volume"},
            {"name": "number", "label": "Number"},
            {"name": "pages", "label": "Pages"},
            {"name": "month", "label": "Month"},
            {"name": "doi", "label": "DOI"},
            {"name": "note", "label": "Note"},
            {"name": "key", "label": "Key"},
        ],
    },
}
