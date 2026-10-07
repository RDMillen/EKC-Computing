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

from database import add_user, find_user_by_email, get_connection, get_room
from helpers import SCHEMA, SEED


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection()
        self.conn.executescript(SCHEMA)
        self.conn.executescript(SEED)

    def test_get_room(self):
        room = get_room(self.conn, 101)
        self.assertEqual(80.0, room["price_per_night"])
        self.assertIsNone(get_room(self.conn, 999))

    def test_add_user_returns_new_id_and_saves(self):
        new_id = add_user(self.conn, "Maria", "maria@example.com", "hash")
        self.assertEqual(3, new_id)
        self.assertEqual("Maria", find_user_by_email(self.conn, "maria@example.com")["name"])

    def test_duplicate_email_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_user(self.conn, "Other James", "james@example.com", "hash")

    def test_find_user_missing(self):
        self.assertIsNone(find_user_by_email(self.conn, "nobody@example.com"))

    def test_injection_attempt_is_stored_as_plain_text(self):
        nasty = "Mary'); DROP TABLE users;--"
        add_user(self.conn, nasty, "bobby@example.com", "hash")
        self.assertEqual(nasty, find_user_by_email(self.conn, "bobby@example.com")["name"])
        tables = {r[0] for r in self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        self.assertIn("users", tables, msg="The users table was dropped. Use ? parameters!")

    def test_injection_in_lookup_finds_nothing(self):
        self.assertIsNone(find_user_by_email(self.conn, "' OR '1'='1"))


if __name__ == "__main__":
    unittest.main()
