import unittest
from unittest.mock import patch

from app import app as flask_app
from entities.reference import Reference


class AppTests(unittest.TestCase):
    def setUp(self):
        flask_app.config["TESTING"] = True
        self.client = flask_app.test_client()

    def test_index_renders_ok(self):
        with patch("app.get_filtered_references", return_value="Ei viitteitä"):
            resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Reference App", resp.data)

    def test_create_book_calls_repository(self):
        called = {}

        def fake_create(citekey, entry_type, data):
            called["citekey"] = citekey
            called["entry_type"] = entry_type
            called["data"] = data

        with patch("app.create_references", side_effect=fake_create):
            resp = self.client.post(
                "/create_references",
                data={
                    "entry_type": "book",
                    "citekey": "ck1",
                    "author": "Auth",
                    "title": "Title",
                    "year": "2024",
                    "publisher": "Pub",
                },
            )

        self.assertEqual(resp.status_code, 302)
        self.assertIn("created=true", resp.location)
        self.assertEqual(called["citekey"], "ck1")
        self.assertEqual(called["entry_type"], "book")
        self.assertEqual(called["data"]["publisher"], "Pub")

    def test_create_missing_required_redirects_with_error(self):
        with patch("app.create_references", return_value=None):
            resp = self.client.post(
                "/create_references",
                data={
                    "entry_type": "book",
                    "citekey": "ck2",
                    "author": "Auth",
                    "title": "Title",
                    "year": "2024",
                    "publisher": "", 
                },
            )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("error=publisher+is+required", resp.location)

    def test_edit_reference_get_not_found(self):
        with patch("app.get_reference_by_key", return_value=None):
            resp = self.client.get("/edit_reference/unknown")
        self.assertEqual(resp.status_code, 404)

    def test_edit_reference_updates_data(self):
        current = {"author": "Old", "title": "OldT", "year": 2020, "publisher": "OldP"}
        ref = Reference("ck3", "book", current)
        updated_storage = {}

        def fake_get(key):
            self.assertEqual(key, "ck3")
            return ref

        def fake_update(citekey, data):
            self.assertEqual(citekey, "ck3")
            updated_storage.update(data)

        with patch("app.get_reference_by_key", side_effect=fake_get), patch(
            "app.update_reference", side_effect=fake_update
        ):
            resp = self.client.post(
                "/edit_reference/ck3",
                data={
                    "entry_type": "book",
                    "citekey": "ck3",
                    "author": "NewA",
                    "title": "NewT",
                    "year": "2021",
                    "publisher": "NewP",
                },
            )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(updated_storage["author"], "NewA")
        self.assertEqual(updated_storage["publisher"], "NewP")
