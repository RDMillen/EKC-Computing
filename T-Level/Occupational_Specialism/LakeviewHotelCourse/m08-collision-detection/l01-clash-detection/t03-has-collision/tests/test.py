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


class TestCollision(unittest.TestCase):
    def setUp(self):
        self.db = make_db()

    def clash(self, room, check_in, check_out):
        return has_collision(self.db, room, check_in, check_out)

    def test_inside_an_existing_stay(self):
        self.assertTrue(self.clash(1, "2026-11-02", "2026-11-03"))

    def test_overlapping_the_start(self):
        self.assertTrue(self.clash(1, "2026-10-30", "2026-11-02"))

    def test_overlapping_the_end(self):
        self.assertTrue(self.clash(1, "2026-11-03", "2026-11-06"))

    def test_surrounding_an_existing_stay(self):
        self.assertTrue(self.clash(1, "2026-10-30", "2026-11-06"))

    def test_identical_dates(self):
        self.assertTrue(self.clash(1, "2026-11-01", "2026-11-04"))

    def test_new_guest_may_arrive_on_the_checkout_day(self):
        self.assertFalse(self.clash(1, "2026-11-04", "2026-11-06"), msg="Back-to-back stays are allowed")

    def test_new_guest_may_leave_on_the_check_in_day(self):
        self.assertFalse(self.clash(1, "2026-10-30", "2026-11-01"), msg="Back-to-back stays are allowed")

    def test_gap_between_bookings(self):
        self.assertFalse(self.clash(1, "2026-11-05", "2026-11-30"))

    def test_other_rooms_are_not_affected(self):
        self.assertFalse(self.clash(3, "2026-11-02", "2026-11-03"))
        self.assertFalse(self.clash(4, "2026-11-01", "2026-11-04"))

    def test_returns_a_boolean(self):
        self.assertIs(True, self.clash(1, "2026-11-02", "2026-11-03"))
        self.assertIs(False, self.clash(3, "2026-11-02", "2026-11-03"))


if __name__ == "__main__":
    unittest.main()
