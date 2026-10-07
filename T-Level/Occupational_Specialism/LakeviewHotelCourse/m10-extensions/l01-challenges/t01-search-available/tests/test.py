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
from dbhelpers import make_db
from search import find_available_rooms


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.db = make_db()   # room 101 is booked 1-4 Nov and 1-3 Dec; room 201 10-12 Nov; room 102 is unavailable

    def numbers(self, check_in, check_out, occupants):
        return [row["number"] for row in find_available_rooms(self.db, check_in, check_out, occupants)]

    def test_booked_and_unavailable_rooms_are_left_out(self):
        self.assertEqual([103, 201, 312], self.numbers("2026-11-02", "2026-11-05", 1))

    def test_capacity_is_respected(self):
        self.assertEqual([201, 312], self.numbers("2026-11-02", "2026-11-05", 3))
        self.assertEqual([201], self.numbers("2026-11-02", "2026-11-05", 4))
        self.assertEqual([], self.numbers("2026-11-02", "2026-11-05", 5))

    def test_back_to_back_dates_free_the_room(self):
        self.assertEqual([101, 103, 201, 312], self.numbers("2026-11-04", "2026-11-06", 1))

    def test_other_bookings_block_their_own_dates(self):
        self.assertEqual([101, 103, 312], self.numbers("2026-11-10", "2026-11-12", 1))

    def test_results_are_cheapest_first(self):
        prices = [row["price_per_night"] for row in find_available_rooms(self.db, "2026-10-01", "2026-10-02", 1)]
        self.assertEqual(sorted(prices), prices)


if __name__ == "__main__":
    unittest.main()
