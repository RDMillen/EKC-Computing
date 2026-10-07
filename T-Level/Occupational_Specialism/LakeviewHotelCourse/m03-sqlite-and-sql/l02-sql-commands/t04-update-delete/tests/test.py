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

from helpers import SCHEMA, SEED


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.executescript(SEED)
    conn.commit()
    return conn
from queries import DELETE_BOOKING, MARK_ROOM_UNAVAILABLE, UPDATE_ROOM_PRICE


class TestUpdateDelete(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()

    def prices(self):
        return dict(self.conn.execute("SELECT number, price_per_night FROM rooms").fetchall())

    def test_update_price_changes_only_one_room(self):
        before = self.prices()
        cursor = self.conn.execute(UPDATE_ROOM_PRICE, (95.0, 101))
        self.assertEqual(1, cursor.rowcount, msg="Exactly one row should be updated. Is there a WHERE clause?")
        after = self.prices()
        self.assertEqual(95.0, after[101])
        for number in (102, 103, 201, 312):
            self.assertEqual(before[number], after[number])

    def test_mark_unavailable(self):
        cursor = self.conn.execute(MARK_ROOM_UNAVAILABLE, (201,))
        self.assertEqual(1, cursor.rowcount)
        self.assertEqual(0, self.conn.execute("SELECT available FROM rooms WHERE number = 201").fetchone()[0])
        self.assertEqual(1, self.conn.execute("SELECT available FROM rooms WHERE number = 101").fetchone()[0])

    def test_delete_booking(self):
        cursor = self.conn.execute(DELETE_BOOKING, (2,))
        self.assertEqual(1, cursor.rowcount)
        ids = [r[0] for r in self.conn.execute("SELECT id FROM bookings ORDER BY id")]
        self.assertEqual([1, 3], ids)


if __name__ == "__main__":
    unittest.main()
