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
from bookings import add_nights, nights_between


class TestDates(unittest.TestCase):
    def test_add_nights(self):
        self.assertEqual("2026-11-04", add_nights("2026-11-01", 3))
        self.assertEqual("2026-11-02", add_nights("2026-11-01", 1))

    def test_month_and_year_boundaries(self):
        self.assertEqual("2027-01-02", add_nights("2026-12-30", 3))
        self.assertEqual("2027-03-01", add_nights("2027-02-28", 1))

    def test_leap_year(self):
        self.assertEqual("2028-03-01", add_nights("2028-02-28", 2))

    def test_result_is_iso_text(self):
        self.assertIsInstance(add_nights("2026-11-01", 3), str)

    def test_nights_between(self):
        self.assertEqual(3, nights_between("2026-11-01", "2026-11-04"))
        self.assertEqual(3, nights_between("2026-12-30", "2027-01-02"))
        self.assertEqual(1, nights_between("2026-11-01", "2026-11-02"))

    def test_nights_between_is_an_int(self):
        self.assertIsInstance(nights_between("2026-11-01", "2026-11-04"), int)

    def test_invalid_dates_raise_value_error(self):
        with self.assertRaises(ValueError):
            add_nights("2026-13-45", 1)
        with self.assertRaises(ValueError):
            nights_between("not-a-date", "2026-11-04")


if __name__ == "__main__":
    unittest.main()
