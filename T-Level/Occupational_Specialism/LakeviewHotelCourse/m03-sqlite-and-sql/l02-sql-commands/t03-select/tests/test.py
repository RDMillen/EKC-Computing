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
from queries import AVAILABLE_ROOMS, ROOMS_FOR_PARTY


class TestSelect(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()

    def test_available_rooms(self):
        rows = [tuple(r) for r in self.conn.execute(AVAILABLE_ROOMS)]
        self.assertEqual([(101, "Single", 80.0), (103, "Double", 110.0),
                          (201, "Family", 180.0), (312, "Suite", 250.0)], rows)

    def test_rooms_for_party(self):
        cases = {(2, 200.0): [(201,), (103,)], (2, 150.0): [(103,)], (4, 500.0): [(201,)], (5, 500.0): []}
        for params, expected in cases.items():
            rows = [tuple(r) for r in self.conn.execute(ROOMS_FOR_PARTY, params)]
            self.assertEqual(expected, rows, msg="Wrong rooms for capacity>=%s, price<=%s" % params)


if __name__ == "__main__":
    unittest.main()
