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
from bookings import create_booking
from dbhelpers import make_db


class TestCreateBooking(unittest.TestCase):
    def setUp(self):
        self.db = make_db()

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]

    def test_booking_is_saved(self):
        before = self.count()
        booking_id = create_booking(self.db, 1, 3, "2026-12-30", 3, 2)
        self.assertEqual(before + 1, self.count())
        row = self.db.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
        self.assertEqual((1, 3, "2026-12-30", "2027-01-02", 2, 330.0),
                         (row["user_id"], row["room_id"], row["check_in"], row["check_out"],
                          row["occupants"], row["total_price"]))

    def test_extra_guests_are_priced(self):
        booking_id = create_booking(self.db, 1, 4, "2026-12-20", 2, 4)
        total = self.db.execute("SELECT total_price FROM bookings WHERE id = ?", (booking_id,)).fetchone()[0]
        self.assertEqual(400.0, total)

    def test_unknown_room(self):
        before = self.count()
        with self.assertRaisesRegex(ValueError, "does not exist"):
            create_booking(self.db, 1, 99, "2026-12-20", 2, 1)
        self.assertEqual(before, self.count())

    def test_unavailable_room(self):
        before = self.count()
        with self.assertRaisesRegex(ValueError, "not available"):
            create_booking(self.db, 1, 2, "2026-12-20", 2, 1)
        self.assertEqual(before, self.count())

    def test_too_many_guests(self):
        before = self.count()
        with self.assertRaisesRegex(ValueError, "sleeps at most 2"):
            create_booking(self.db, 1, 3, "2026-12-20", 2, 3)
        self.assertEqual(before, self.count())

    def test_invalid_stay_length_is_not_saved(self):
        before = self.count()
        with self.assertRaises(ValueError):
            create_booking(self.db, 1, 3, "2026-12-20", 0, 1)
        self.assertEqual(before, self.count())


if __name__ == "__main__":
    unittest.main()
