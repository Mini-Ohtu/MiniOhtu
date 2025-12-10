from unittest.mock import patch

from citekey_service import build_base_citekey, generate_citekey


@patch("citekey_service.secrets.choice", return_value="Best")
def test_build_base_citekey_uses_lastname_year_and_random_significant_word(choice_mock):
    citekey = build_base_citekey("John Smith", 2020, "The best book")
    assert citekey == "Smith2020Best"
    choice_mock.assert_called_once_with(["Best", "Book"])


@patch("citekey_service.secrets.choice", return_value="Molecular")
def test_build_base_citekey_supports_comma_author_format(choice_mock):
    citekey = build_base_citekey(
        "Watson, James D. and Crick, Francis", 1953, "Molecular Structure of Nucleic Acids"
    )
    assert citekey == "Watson1953Molecular"
    choice_mock.assert_called_once_with(["Molecular", "Structure", "Nucleic", "Acids"])


@patch("citekey_service.secrets.choice", return_value="Analysis")
def test_build_base_citekey_skips_stop_words(choice_mock):
    citekey = build_base_citekey("Jane Doe", 2024, "The Analysis of Big Data")
    assert citekey == "Doe2024Analysis"
    choice_mock.assert_called_once_with(["Analysis", "Big", "Data"])


@patch("citekey_service.secrets.choice", return_value="Best")
def test_generate_citekey_appends_suffix_on_collision(choice_mock):
    existing = {"Smith2020Best", "Smith2020Best#1"}

    def exists_fn(key):
        return key in existing

    citekey = generate_citekey("John Smith", 2020, "The best book", exists_fn)
    assert citekey == "Smith2020Best#2"
    choice_mock.assert_called_once_with(["Best", "Book"])


def test_generate_citekey_falls_back_to_ref_when_missing_data():
    def exists_fn(key):
        return key == "ref"

    citekey = generate_citekey("", "", "", exists_fn)
    assert citekey == "ref#1"
