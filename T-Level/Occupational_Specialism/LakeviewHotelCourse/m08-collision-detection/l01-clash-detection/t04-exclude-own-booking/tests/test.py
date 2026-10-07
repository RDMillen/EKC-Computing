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
from bookings import has_collision
from dbhelpers import make_db


class TestExclude(unittest.TestCase):
    def setUp(self):
        self.db = make_db()

    def test_default_still_detects_clashes(self):
        self.assertTrue(has_collision(self.db, 1, "2026-11-02", "2026-11-03"))

    def test_booking_does_not_clash_with_itself(self):
        self.assertFalse(has_collision(self.db, 1, "2026-11-01", "2026-11-05", exclude_booking_id=1),
                         msg="Booking 1 is being edited, so it must be ignored")

    def test_other_bookings_still_clash(self):
        self.assertTrue(has_collision(self.db, 1, "2026-12-02", "2026-12-04", exclude_booking_id=1),
                        msg="Booking 3 is a different booking and still counts")

    def test_excluding_an_unrelated_booking_changes_nothing(self):
        self.assertTrue(has_collision(self.db, 1, "2026-11-02", "2026-11-03", exclude_booking_id=3))

    def test_none_means_exclude_nothing(self):
        self.assertTrue(has_collision(self.db, 1, "2026-11-01", "2026-11-04", exclude_booking_id=None))


if __name__ == "__main__":
    unittest.main()
