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