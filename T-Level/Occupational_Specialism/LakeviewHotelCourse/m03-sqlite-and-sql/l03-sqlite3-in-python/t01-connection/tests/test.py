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

from database import get_connection
from helpers import SCHEMA, SEED


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection()
        self.conn.executescript(SCHEMA)
        self.conn.executescript(SEED)

    def test_returns_connection(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_rows_can_be_read_by_column_name(self):
        row = self.conn.execute("SELECT number, room_type FROM rooms WHERE number = 101").fetchone()
        self.assertEqual("Single", row["room_type"], msg="Set conn.row_factory = sqlite3.Row")

    def test_foreign_keys_are_enforced(self):
        with self.assertRaises(sqlite3.IntegrityError, msg="Turn on PRAGMA foreign_keys"):
            self.conn.execute("INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price) "
                              "VALUES (99, 99, '2026-01-01', '2026-01-02', 1, 10)")


if __name__ == "__main__":
    unittest.main()
