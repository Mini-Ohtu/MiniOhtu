import os
import unittest
from types import SimpleNamespace
from unittest.mock import mock_open, patch

import db_helper


class FakeResult:
    def __init__(self, rows=None):
        self._rows = rows or []

    def fetchall(self):
        return list(self._rows)


class FakeSession:
    def __init__(self):
        self.executes = []
        self.commit_count = 0

    def execute(self, sql, params=None):
        self.executes.append((str(sql), params or {}))
        return FakeResult()

    def commit(self):
        self.commit_count += 1


class DbHelperTests(unittest.TestCase):
    def setUp(self):
        self.fake_session = FakeSession()
        db_helper.db = SimpleNamespace(session=self.fake_session)

    def test_reset_db_executes_delete(self):
        db_helper.reset_db()
        self.assertTrue(self.fake_session.executes)
        sql_text, _ = self.fake_session.executes[0]
        self.assertIn("DELETE FROM bibtex_references", sql_text)
        self.assertEqual(self.fake_session.commit_count, 1)

    def test_setup_db_drops_existing_and_creates_schema(self):
        schema_sql = "CREATE TABLE example(id INT);"
        with patch("db_helper._db_backend", return_value="postgresql"), patch("db_helper.tables", return_value=["old1", "old2"]), patch("db_helper.open", mock_open(read_data=schema_sql), create=True):
            db_helper.setup_db()

        executed = [sql for sql, _ in self.fake_session.executes]
        self.assertGreaterEqual(len(executed), 3)
        self.assertIn("DROP TABLE old1", executed[0])
        self.assertIn("DROP TABLE old2", executed[1])
        self.assertIn("CREATE TABLE example", executed[-1])
        self.assertEqual(self.fake_session.commit_count, 2)
