import unittest

from entities.reference import Reference
from util import validate_reference_year, UserInputError


class TestReferenceHelpers(unittest.TestCase):
    def test_reference_sets_attributes_from_data(self):
        ref = Reference("ck1", "book", {"author": "A U Thor", "year": 2024})
        self.assertEqual(ref.author, "A U Thor")
        self.assertEqual(ref.year, 2024)
        self.assertEqual(ref.data["year"], 2024)

    def test_optional_year_allows_empty(self):
        self.assertIsNone(validate_reference_year("", required=False))
        self.assertIsNone(validate_reference_year(None, required=False))

    def test_optional_year_still_validates_numbers(self):
        self.assertEqual(validate_reference_year("2020", required=False), 2020)

    def test_optional_year_rejects_non_numeric(self):
        with self.assertRaises(UserInputError):
            validate_reference_year("not-a-number", required=False)

