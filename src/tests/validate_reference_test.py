import unittest
from util import validate_reference_title, validate_reference_year, UserInputError


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
