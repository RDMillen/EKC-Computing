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
from bookings import update_booking
from dbhelpers import make_db


class TestUpdateBooking(unittest.TestCase):
    def setUp(self):
        self.db = make_db()   # booking 1: user 1, room 1 (101, sleeps 1, GBP 80), 2026-11-01 to 2026-11-04

    def row(self, booking_id=1):
        return self.db.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()

    def test_dates_and_price_are_recalculated(self):
        update_booking(self.db, 1, 1, "2026-11-02", 5, 1)
        row = self.row()
        self.assertEqual("2026-11-02", row["check_in"])
        self.assertEqual("2026-11-07", row["check_out"])
        self.assertEqual(400.0, row["total_price"])

    def test_changes_are_committed(self):
        update_booking(self.db, 1, 1, "2026-11-02", 5, 1)
        self.db.rollback()
        self.assertEqual("2026-11-07", self.row()["check_out"], msg="Call db.commit() after the UPDATE")

    def test_other_bookings_are_untouched(self):
        before = tuple(self.row(2))
        update_booking(self.db, 1, 1, "2026-11-02", 5, 1)
        self.assertEqual(before, tuple(self.row(2)))

    def test_missing_booking(self):
        with self.assertRaises(LookupError):
            update_booking(self.db, 99, 1, "2026-11-02", 2, 1)

    def test_someone_elses_booking(self):
        before = tuple(self.row())
        with self.assertRaises(PermissionError):
            update_booking(self.db, 1, 2, "2026-11-02", 2, 1)
        self.assertEqual(before, tuple(self.row()))

    def test_too_many_guests(self):
        before = tuple(self.row())
        with self.assertRaisesRegex(ValueError, "sleeps at most 1"):
            update_booking(self.db, 1, 1, "2026-11-02", 2, 2)
        self.assertEqual(before, tuple(self.row()))

    def test_bad_stay_length(self):
        with self.assertRaises(ValueError):
            update_booking(self.db, 1, 1, "2026-11-02", 0, 1)


if __name__ == "__main__":
    unittest.main()
