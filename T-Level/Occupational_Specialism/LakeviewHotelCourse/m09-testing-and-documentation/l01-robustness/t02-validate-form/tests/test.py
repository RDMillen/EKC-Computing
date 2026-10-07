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
from datetime import date

from helpers import add_booking, cleanup, login, make_client, query
from validation import validate_booking_form

TODAY = date(2026, 10, 7)


def form(**changes):
    data = {"check_in": "2026-12-01", "nights": "3", "occupants": "2"}
    data.update(changes)
    return data


class TestValidation(unittest.TestCase):
    def check(self, expected, **changes):
        self.assertEqual(expected, validate_booking_form(form(**changes), today=TODAY), msg=str(changes))

    def test_valid_form(self):
        self.check([])

    def test_today_is_allowed(self):
        self.check([], check_in="2026-10-07")

    def test_yesterday_is_not(self):
        self.check(["Check-in cannot be in the past"], check_in="2026-10-06")

    def test_date_format(self):
        for bad in ("01/12/2026", "tomorrow", "", "2026-02-30", "2026-13-01"):
            self.check(["Please enter the check-in date as YYYY-MM-DD"], check_in=bad)

    def test_missing_fields(self):
        self.assertEqual(3, len(validate_booking_form({}, today=TODAY)))

    def test_nights_boundaries(self):
        self.check([], nights="1")
        self.check([], nights="30")
        self.check(["Nights must be between 1 and 30"], nights="0")
        self.check(["Nights must be between 1 and 30"], nights="31")
        self.check(["Nights must be between 1 and 30"], nights="-2")

    def test_nights_must_be_a_whole_number(self):
        for bad in ("abc", "1.5", "", " "):
            self.check(["Nights must be a whole number"], nights=bad)

    def test_occupants(self):
        self.check(["At least one occupant is required"], occupants="0")
        self.check(["Occupants must be a whole number"], occupants="two")
        self.check([], occupants="1")

    def test_every_problem_is_reported_in_order(self):
        result = validate_booking_form({"check_in": "x", "nights": "y", "occupants": "z"}, today=TODAY)
        self.assertEqual(["Please enter the check-in date as YYYY-MM-DD", "Nights must be a whole number",
                          "Occupants must be a whole number"], result)

    def test_default_today_is_the_real_date(self):
        self.assertEqual([], validate_booking_form(form(check_in="2999-01-01")))


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        login(self.client, 1)

    def tearDown(self):
        cleanup(self.path)

    def test_bad_form_shows_every_message(self):
        body = self.client.post("/book/3", data={"check_in": "nope", "nights": "abc", "occupants": "0"}).get_data(as_text=True)
        self.assertIn("Please enter the check-in date as YYYY-MM-DD", body)
        self.assertIn("Nights must be a whole number", body)
        self.assertIn("At least one occupant is required", body)
        self.assertEqual(0, query("SELECT COUNT(*) FROM bookings")[0][0])

    def test_past_date_is_refused(self):
        body = self.client.post("/book/3", data={"check_in": "2020-01-01", "nights": "2", "occupants": "1"}).get_data(as_text=True)
        self.assertIn("Check-in cannot be in the past", body)

    def test_good_form_still_books(self):
        response = self.client.post("/book/3", data={"check_in": "2030-05-10", "nights": "3", "occupants": "2"})
        self.assertEqual(302, response.status_code)

    def test_edit_form_is_validated_too(self):
        mine = add_booking(1, 3, "2030-06-01", "2030-06-03", 1, 220.0)
        body = self.client.post("/bookings/%d/edit" % mine,
                                data={"check_in": "2030-06-01", "nights": "0", "occupants": "1"}).get_data(as_text=True)
        self.assertIn("Nights must be between 1 and 30", body)

    def test_collisions_are_still_reported(self):
        add_booking(2, 3, "2030-05-10", "2030-05-13", 1, 330.0)
        body = self.client.post("/book/3", data={"check_in": "2030-05-11", "nights": "1", "occupants": "1"}).get_data(as_text=True)
        self.assertIn("Those dates are already booked", body)


if __name__ == "__main__":
    unittest.main()
