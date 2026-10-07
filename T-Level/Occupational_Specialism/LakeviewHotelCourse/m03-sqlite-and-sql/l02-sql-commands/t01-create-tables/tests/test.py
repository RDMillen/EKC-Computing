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

from queries import SCHEMA

EXPECTED = {
    "users": {"id", "name", "email", "password_hash"},
    "rooms": {"id", "number", "room_type", "capacity", "price_per_night", "available"},
    "bookings": {"id", "user_id", "room_id", "check_in", "check_out", "occupants", "total_price"},
}


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def test_tables_exist(self):
        names = {r[0] for r in self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")}
        self.assertEqual({"users", "rooms", "bookings"}, names)

    def test_columns(self):
        for table, columns in EXPECTED.items():
            got = {r[1] for r in self.conn.execute("PRAGMA table_info(%s)" % table)}
            self.assertEqual(columns, got, msg="Wrong columns in %s" % table)

    def test_primary_keys(self):
        for table in EXPECTED:
            pk = [r[1] for r in self.conn.execute("PRAGMA table_info(%s)" % table) if r[5]]
            self.assertEqual(["id"], pk, msg="%s should have id as its primary key" % table)

    def test_foreign_keys(self):
        targets = {r[2] for r in self.conn.execute("PRAGMA foreign_key_list(bookings)")}
        self.assertEqual({"users", "rooms"}, targets, msg="bookings needs foreign keys to users and rooms")

    def test_email_is_unique(self):
        self.conn.execute("INSERT INTO users (name, email, password_hash) VALUES ('A', 'a@x.com', 'h')")
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("INSERT INTO users (name, email, password_hash) VALUES ('B', 'a@x.com', 'h')")

    def test_required_columns(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("INSERT INTO users (name, email, password_hash) VALUES (NULL, 'b@x.com', 'h')")

    def test_room_defaults_and_checks(self):
        self.conn.execute("INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (1, 'S', 1, 50)")
        self.assertEqual(1, self.conn.execute("SELECT available FROM rooms").fetchone()[0],
                         msg="available should default to 1")
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (2, 'S', 0, 50)")

    def test_booking_needs_real_user_and_room(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price) "
                              "VALUES (9, 9, '2026-01-01', '2026-01-02', 1, 10)")


if __name__ == "__main__":
    unittest.main()
