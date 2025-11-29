import json
import unittest
from types import SimpleNamespace

import repositories.reference_repository as reference_repository
from entities.reference import Reference


class FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return list(self._rows)

    def fetchone(self):
        return self._rows[0] if self._rows else None


class FakeSession:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.last_sql = None
        self.last_params = None
        self.committed = False

    def execute(self, sql, params=None):
        self.last_sql = sql
        self.last_params = params or {}
        return FakeResult(self.rows)

    def commit(self):
        self.committed = True


class ReferenceRepositoryTests(unittest.TestCase):
    def setUp(self):
        # Replace db.session with a controllable fake
        self.fake_session = FakeSession()
        reference_repository.db = SimpleNamespace(session=self.fake_session)
        self._original_get_by_key = reference_repository.get_reference_by_key

    def tearDown(self):
        reference_repository.get_reference_by_key = self._original_get_by_key

    def test_get_references_parses_json_payload(self):
        payload = {"author": "A", "title": "T", "year": 2024}
        self.fake_session.rows = [
            ("ck1", "book", json.dumps(payload)),
        ]
        refs = reference_repository.get_references()
        self.assertIsInstance(refs[0], Reference)
        self.assertEqual(refs[0].citekey, "ck1")
        self.assertEqual(refs[0].data["author"], "A")

    def test_update_reference_merges_and_cleans(self):
        existing_ref = Reference("ck2", "book", {"author": "Old", "note": "keep"})

        def fake_get_by_key(citekey):
            return existing_ref

        reference_repository.get_reference_by_key = fake_get_by_key
        reference_repository.update_reference(
            "ck2", {"author": " New ", "title": "Title", "note": ""}
        )
        sent_data = json.loads(self.fake_session.last_params["data"])
        self.assertEqual(sent_data["author"], "New")
        self.assertEqual(sent_data["title"], "Title")
        self.assertEqual(sent_data["note"], "keep")

    def test_get_references_returns_no_results_message(self):
        self.fake_session.rows = []
        result = reference_repository.get_references()
        self.assertEqual(result, "Ei viitteitä")

    def test_get_references_handles_invalid_and_non_dict_payloads(self):
        self.fake_session.rows = [
            ("ck1", "misc", "not-json"),
            ("ck2", "misc", json.dumps(["unexpected", "list"])),
        ]
        references = reference_repository.get_references()
        self.assertEqual(len(references), 2)
        self.assertEqual(references[0].data, {})
        self.assertEqual(references[1].data, {})

    def test_create_references_cleans_and_commits(self):
        reference_repository.create_references(
            "ck3",
            "article",
            {"author": "  Name  ", "empty": "   ", "missing": None, "year": 2020},
        )
        sent = json.loads(self.fake_session.last_params["data"])
        self.assertEqual(sent, {"author": "Name", "year": 2020})
        self.assertIn("INSERT INTO bibtex_references", str(self.fake_session.last_sql))
        self.assertTrue(self.fake_session.committed)

    def test_delete_reference_executes_delete(self):
        reference_repository.delete_reference("ck4")
        self.assertIn("DELETE FROM bibtex_references", str(self.fake_session.last_sql))
        self.assertEqual(self.fake_session.last_params["citekey"], "ck4")
        self.assertTrue(self.fake_session.committed)

    def test_update_reference_without_existing_starts_from_empty(self):
        reference_repository.get_reference_by_key = lambda citekey: None
        reference_repository.update_reference(
            "ck5", {"author": "  Author ", "notes": None, "title": " Title "}
        )
        sent_data = json.loads(self.fake_session.last_params["data"])
        self.assertEqual(sent_data, {"author": "Author", "title": "Title"})
        self.assertTrue(self.fake_session.committed)

    def test_get_reference_by_key_returns_none_when_not_found(self):
        self.fake_session.rows = []
        reference = reference_repository.get_reference_by_key("missing")
        self.assertIsNone(reference)

    def test_get_reference_by_key_handles_broken_payload(self):
        self.fake_session.rows = [("ck6", "article", "invalid{json")]
        reference = reference_repository.get_reference_by_key("ck6")
        self.assertIsInstance(reference, Reference)
        self.assertEqual(reference.data, {})
