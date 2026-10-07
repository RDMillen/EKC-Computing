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
from bookings import calculate_price


class TestPrice(unittest.TestCase):
    def test_two_guests_pay_the_base_rate(self):
        self.assertEqual(300.0, calculate_price(100.0, 3, 2))

    def test_one_guest_is_not_discounted(self):
        self.assertEqual(300.0, calculate_price(100.0, 3, 1))

    def test_extra_guests_pay_a_supplement(self):
        self.assertEqual(240.0, calculate_price(100.0, 2, 4))
        self.assertEqual(90.0, calculate_price(80.0, 1, 3))

    def test_rounding(self):
        self.assertEqual(269.97, calculate_price(89.99, 3, 2))

    def test_at_least_one_night(self):
        with self.assertRaises(ValueError):
            calculate_price(100.0, 0, 2)
        with self.assertRaises(ValueError):
            calculate_price(100.0, -1, 2)

    def test_at_least_one_guest(self):
        with self.assertRaises(ValueError):
            calculate_price(100.0, 2, 0)


if __name__ == "__main__":
    unittest.main()
