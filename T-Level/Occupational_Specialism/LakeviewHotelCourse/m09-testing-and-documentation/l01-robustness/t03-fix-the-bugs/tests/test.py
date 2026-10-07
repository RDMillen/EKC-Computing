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
from bugs import calculate_price, nights_between, overlaps


class TestBugs(unittest.TestCase):
    def test_nights_between(self):
        self.assertEqual(3, nights_between("2026-11-01", "2026-11-04"))
        self.assertEqual(1, nights_between("2026-11-01", "2026-11-02"))

    def test_price_for_two_guests_is_the_base_rate(self):
        self.assertEqual(200.0, calculate_price(100.0, 2, 2))

    def test_price_for_extra_guests(self):
        self.assertEqual(220.0, calculate_price(100.0, 2, 3))
        self.assertEqual(100.0, calculate_price(100.0, 1, 1))

    def test_back_to_back_stays_do_not_overlap(self):
        self.assertFalse(overlaps("2026-11-01", "2026-11-04", "2026-11-04", "2026-11-06"))
        self.assertFalse(overlaps("2026-11-04", "2026-11-06", "2026-11-01", "2026-11-04"))

    def test_real_overlaps_are_found(self):
        self.assertTrue(overlaps("2026-11-01", "2026-11-04", "2026-11-03", "2026-11-06"))
        self.assertTrue(overlaps("2026-11-02", "2026-11-03", "2026-11-01", "2026-11-04"))
        self.assertTrue(overlaps("2026-11-01", "2026-11-04", "2026-11-01", "2026-11-04"))


if __name__ == "__main__":
    unittest.main()
