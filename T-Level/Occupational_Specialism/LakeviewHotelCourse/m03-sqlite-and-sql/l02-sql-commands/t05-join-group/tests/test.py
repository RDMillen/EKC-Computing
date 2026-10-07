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
from queries import BOOKING_DETAILS, ROOM_BOOKING_COUNTS


class TestJoins(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()

    def test_booking_details(self):
        rows = [tuple(r) for r in self.conn.execute(BOOKING_DETAILS)]
        self.assertEqual([
            (1, "James Sunderland", 101, "2026-11-01", "2026-11-04", 240.0),
            (2, "Mary Sunderland", 201, "2026-11-10", "2026-11-12", 360.0),
            (3, "James Sunderland", 101, "2026-12-01", "2026-12-03", 160.0),
        ], rows)

    def test_room_booking_counts_include_empty_rooms(self):
        rows = [tuple(r) for r in self.conn.execute(ROOM_BOOKING_COUNTS)]
        self.assertEqual([(101, 2), (102, 0), (103, 0), (201, 1), (312, 0)], rows,
                         msg="Use a LEFT JOIN so rooms with no bookings still appear")


if __name__ == "__main__":
    unittest.main()
