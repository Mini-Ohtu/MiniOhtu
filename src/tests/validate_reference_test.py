import unittest
from util import validate_reference_title, validate_reference_year, UserInputError
from entities.reference import Reference

class TestRerence(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_title_does_not_raise_error(self):
        validate_reference_title("Test title")

    def test_too_short_or_long_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference_title("")

        with self.assertRaises(UserInputError):
            validate_reference_title("koodaa" * 200)

    def test_year_missing_or_not_integer_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference_year("")

        with self.assertRaises(UserInputError):
            validate_reference_year("nineteen ninety")

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

