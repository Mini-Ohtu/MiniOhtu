import unittest
from unittest.mock import patch

from doi_service import (
    DoiServiceError,
    fetch_reference_from_doi,
    parse_bibtex_entry,
)


SAMPLE_BIBTEX = """@article{Watson_1953,
    doi = {10.1038/nature123},
    url = {https://doi.org/10.1038%2Fnature123},
    year = 1953,
    month = {apr},
    publisher = {Springer Science and Business Media LLC},
    volume = {171},
    number = {4356},
    pages = {737--738},
    author = {J. D. WATSON and F. H. C. CRICK},
    title = {Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid},
    journal = {Nature}
}
"""


class DoiServiceTests(unittest.TestCase):
    def test_parse_bibtex_entry_extracts_fields(self):
        parsed = parse_bibtex_entry(SAMPLE_BIBTEX)
        self.assertEqual(parsed["entry_type"], "article")
        self.assertEqual(parsed["citekey"], "Watson_1953")
        self.assertEqual(parsed["data"]["doi"], "10.1038/nature123")
        self.assertEqual(parsed["data"]["year"], 1953)
        self.assertIn("title", parsed["data"])

    def test_fetch_reference_from_doi_calls_doi_service(self):
        called = {}

        class FakeResponse:
            status_code = 200
            text = SAMPLE_BIBTEX

        def fake_get(url, headers=None, timeout=None):
            called["url"] = url
            called["headers"] = headers or {}
            called["timeout"] = timeout
            return FakeResponse()

        with patch("doi_service.requests.get", side_effect=fake_get):
            parsed = fetch_reference_from_doi("10.1038/nature123")

        self.assertEqual(parsed["citekey"], "Watson_1953")
        self.assertEqual(
            called["url"],
            "https://doi.org/10.1038/nature123",
        )
        self.assertEqual(
            called["headers"].get("Accept"),
            "application/x-bibtex",
        )
        self.assertGreaterEqual(called["timeout"], 5)

    def test_fetch_reference_from_doi_raises_on_error(self):
        class FakeResponse:
            status_code = 404
            text = ""

        with patch("doi_service.requests.get", return_value=FakeResponse()):
            with self.assertRaises(DoiServiceError):
                fetch_reference_from_doi("10.9999/unknown")

    def test_parse_handles_single_line_with_commas(self):
        inline = (
            "@article{Watson_1953,"
            " title={Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid},"
            " volume={171}, ISSN={1476-4687}, url={http://dx.doi.org/10.1038/171737a0},"
            " DOI={10.1038/171737a0}, number={4356}, journal={Nature},"
            " publisher={Springer Science and Business Media LLC},"
            " author={WATSON, J. D. and CRICK, F. H. C.}, year={1953}, month=apr, pages={737–738}"
            "}"
        )
        parsed = parse_bibtex_entry(inline)
        data = parsed["data"]
        self.assertEqual(data["title"], "Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid")
        self.assertEqual(data["doi"], "10.1038/171737a0")
        self.assertEqual(data["year"], 1953)
        self.assertEqual(data["number"], 4356)
        self.assertEqual(data["journal"], "Nature")


if __name__ == "__main__":
    unittest.main()
