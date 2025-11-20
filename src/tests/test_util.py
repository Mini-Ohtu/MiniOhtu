import unittest
# pylint: disable=R0402
import src.util as util

class TestUtil(unittest.TestCase):
    def test_empty_title(self):
        got_error = False
        try:
            util.validate_reference_title("")
        except util.UserInputError:
            got_error = True
        self.assertTrue(got_error, "Expected UserInputError for empty title")
