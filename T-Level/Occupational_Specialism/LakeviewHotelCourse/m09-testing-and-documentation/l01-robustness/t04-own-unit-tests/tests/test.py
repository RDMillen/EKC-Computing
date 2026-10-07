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
import importlib
import io

import bookings

REAL = bookings.calculate_price


def extra_from_one(price, nights, occupants):
    if nights < 1 or occupants < 1:
        raise ValueError("bad")
    return round((price + max(0, occupants - 1) * 10.0) * nights, 2)


def one_guest_discount(price, nights, occupants):
    if nights < 1 or occupants < 1:
        raise ValueError("bad")
    return round((price + (occupants - 2) * 10.0) * nights, 2)


def no_validation(price, nights, occupants):
    return round((price + max(0, occupants - 2) * 10.0) * nights, 2)


def supplement_once(price, nights, occupants):
    if nights < 1 or occupants < 1:
        raise ValueError("bad")
    return round(price * nights + max(0, occupants - 2) * 10.0, 2)


def run_student_tests(price_function=REAL):
    module = importlib.import_module("test_pricing")
    had_name = hasattr(module, "calculate_price")
    bookings.calculate_price = price_function
    if had_name:
        module.calculate_price = price_function
    try:
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        return suite.countTestCases(), result, stream.getvalue()
    finally:
        bookings.calculate_price = REAL
        if had_name:
            module.calculate_price = REAL


class TestYourTests(unittest.TestCase):
    def test_at_least_four_tests(self):
        count, _, _ = run_student_tests()
        self.assertGreaterEqual(count, 4, msg="Write at least four test methods (you have %d)" % count)

    def test_your_tests_pass_on_the_correct_code(self):
        _, result, output = run_student_tests()
        self.assertTrue(result.wasSuccessful(),
                        msg="Your tests should all pass when calculate_price is correct:\n" + output)

    def check_catches(self, broken, description):
        _, result, _ = run_student_tests(broken)
        self.assertFalse(result.wasSuccessful(), msg="None of your tests noticed this bug: " + description)

    def test_catches_extra_guests_counted_from_one(self):
        self.check_catches(extra_from_one, "extra guests counted from 1 guest instead of from 3")

    def test_catches_discount_for_one_guest(self):
        self.check_catches(one_guest_discount, "a single guest is given a discount")

    def test_catches_missing_validation(self):
        self.check_catches(no_validation, "0 nights does not raise a ValueError")

    def test_catches_supplement_charged_once(self):
        self.check_catches(supplement_once, "the extra guest supplement is charged once, not every night")


if __name__ == "__main__":
    unittest.main()
