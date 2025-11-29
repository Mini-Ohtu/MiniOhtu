import unittest

from entities.reference import Reference
from util import validate_reference_year


class TestReferenceHelpers(unittest.TestCase):
    def test_reference_str_contains_citekey_and_data(self):
        ref = Reference("ck1", "book", {"author": "A U Thor", "title": "Book Title"})
        rendered = str(ref)
        self.assertIn("book:ck1", rendered)
        self.assertIn("Book Title", rendered)

    def test_reference_defaults_to_empty_data_dict(self):
        ref = Reference("ck2", "misc", None)
        self.assertEqual(ref.data, {})
        self.assertFalse(hasattr(ref, "title"))

    def test_validate_reference_year_strips_whitespace(self):
        self.assertEqual(validate_reference_year("   1999   "), 1999)
