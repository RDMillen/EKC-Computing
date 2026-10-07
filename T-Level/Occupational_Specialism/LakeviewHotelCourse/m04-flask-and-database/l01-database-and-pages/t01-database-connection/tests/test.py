import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))

# Keep failure messages short: never print a whole HTML page back at the student.
_original_assert_in = unittest.TestCase.assertIn
_original_assert_not_in = unittest.TestCase.assertNotIn



def _join(msg, hint):
    if not msg:
        return hint
    msg = str(msg).rstrip()
    return msg + (" " if msg.endswith((".", "!", "?", ":")) else ". ") + hint


def _short_assert_in(self, member, container, msg=None):
    if isinstance(container, str) and len(container) > 200:
        if member not in container:
            hint = "The page should contain %r, but it does not." % (member,)
            self.fail(_join(msg, hint))
    else:
        _original_assert_in(self, member, container, msg)


def _short_assert_not_in(self, member, container, msg=None):
    if isinstance(container, str) and len(container) > 200:
        if member in container:
            hint = "The page should not contain %r, but it does." % (member,)
            self.fail(_join(msg, hint))
    else:
        _original_assert_not_in(self, member, container, msg)


unittest.TestCase.assertIn = _short_assert_in
unittest.TestCase.assertNotIn = _short_assert_not_in
import sqlite3
import tempfile

from flask import Flask

from db import close_db, get_db, init_db


class TestDb(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.app = Flask(__name__)
        self.app.config["DATABASE"] = self.path
        self.app.teardown_appcontext(close_db)

    def tearDown(self):
        try:
            os.remove(self.path)
        except OSError:
            pass

    def test_one_connection_per_context(self):
        with self.app.app_context():
            self.assertIs(get_db(), get_db(), msg="get_db() must reuse the connection stored on g")

    def test_rows_can_be_read_by_name(self):
        with self.app.app_context():
            row = get_db().execute("SELECT 1 AS one").fetchone()
            self.assertEqual(1, row["one"])

    def test_foreign_keys_on(self):
        with self.app.app_context():
            self.assertEqual(1, get_db().execute("PRAGMA foreign_keys").fetchone()[0])

    def test_connection_is_closed_after_the_context(self):
        with self.app.app_context():
            connection = get_db()
        with self.assertRaises(sqlite3.ProgrammingError, msg="close_db() should close the connection"):
            connection.execute("SELECT 1")

    def test_init_db_creates_tables(self):
        with self.app.app_context():
            init_db()
            names = {r[0] for r in get_db().execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")}
        self.assertEqual({"users", "rooms", "bookings"}, names)


if __name__ == "__main__":
    unittest.main()
