from citekey_service import build_base_citekey, generate_citekey


def test_build_base_citekey_uses_lastname_year_and_title_initials():
    citekey = build_base_citekey("John Smith", 2020, "The best book")
    assert citekey == "Smith2020tbb"


def test_build_base_citekey_supports_comma_author_format():
    citekey = build_base_citekey(
        "Watson, James D. and Crick, Francis", 1953, "Molecular Structure of Nucleic Acids"
    )
    assert citekey == "Watson1953msona"


def test_generate_citekey_appends_suffix_on_collision():
    existing = {"Smith2020tbb", "Smith2020tbb1"}

    def exists_fn(key):
        return key in existing

    citekey = generate_citekey("John Smith", 2020, "The best book", exists_fn)
    assert citekey == "Smith2020tbb2"


def test_generate_citekey_falls_back_to_ref_when_missing_data():
    def exists_fn(key):
        return key == "ref"

    citekey = generate_citekey("", "", "", exists_fn)
    assert citekey == "ref1"
