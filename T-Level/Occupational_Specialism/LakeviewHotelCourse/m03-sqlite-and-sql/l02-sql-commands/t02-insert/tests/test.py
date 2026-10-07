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

from queries import INSERT_ROOM, INSERT_USER, SCHEMA


class TestInsert(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.executescript(SCHEMA)

    def test_insert_room(self):
        self.conn.execute(INSERT_ROOM, (401, "Penthouse", 4, 399.0))
        row = self.conn.execute(
            "SELECT number, room_type, capacity, price_per_night, available FROM rooms").fetchone()
        self.assertEqual((401, "Penthouse", 4, 399.0, 1), row)

    def test_insert_user(self):
        self.conn.execute(INSERT_USER, ("Maria", "maria@example.com", "hash"))
        row = self.conn.execute("SELECT name, email, password_hash FROM users").fetchone()
        self.assertEqual(("Maria", "maria@example.com", "hash"), row)

    def test_parameters_not_pasted_in(self):
        self.assertEqual(4, INSERT_ROOM.count("?"), msg="INSERT_ROOM needs four ? parameters")
        self.assertEqual(3, INSERT_USER.count("?"), msg="INSERT_USER needs three ? parameters")


if __name__ == "__main__":
    unittest.main()
